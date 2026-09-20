"""
Step 6 — Evaluation: F1-score, IoU, mAP (threshold sweep 0.05–0.95, step 0.05).
Operating threshold = the threshold maximizing validation IoU → locked with the
final model. Writes Model/metrics.json in the exact schema served by /api/metrics.

Status: v1 — ported from notebook.  Run AFTER train.py, on the SAME session's
validation split (same seed) or a persisted split index (v2 will persist it).
"""
import json
import numpy as np
from config import IMAGES_DIR, MASKS_DIR, MODELS_DIR, METRICS_OUT
import tensorflow as tf

THRESHOLDS = np.arange(0.05, 1.0, 0.05)          # thesis spec: 0.05 → 0.95
SPLIT_SEED = 42


def prf(y, p, t):
    """Per-patch precision/recall/F1/IoU at threshold t (mangrove = positive)."""
    pred = p >= t
    tp = int((pred & (y == 1)).sum())
    fp = int((pred & (y == 0)).sum())
    fn = int((~pred & (y == 1)).sum())
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec  = tp / (tp + fn) if tp + fn else 0.0
    f1   = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0
    iou  = tp / (tp + fp + fn) if tp + fp + fn else 0.0
    return tp, fp, fn, prec, rec, f1, iou


def main():
    # rebuild the SAME 80/20 split as train.py (shared seed)
    X = np.stack([np.load(p) for p in sorted(IMAGES_DIR.glob("*.npy"))]).astype("float32")
    Y = np.stack([np.load(MASKS_DIR / p.name)
                  for p in sorted(IMAGES_DIR.glob("*.npy"))]).astype("float32")
    rng = np.random.default_rng(SPLIT_SEED)
    idx = rng.permutation(len(X))
    Xva, Yva = X[idx[int(len(X) * 0.8):]], Y[idx[int(len(X) * 0.8):]]

    model = tf.keras.models.load_model(MODELS_DIR / "final_model.keras")
    probs = model.predict(Xva, verbose=0).squeeze(-1)
    ys = Yva.squeeze(-1)

    # threshold sweep → PR curve + best-IoU operating threshold
    pr, best_t, best_iou = {}, 0.5, -1.0
    cm = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}
    for t in THRESHOLDS:
        tp = fp = fn = 0
        f1s, ious = [], []
        for y, p in zip(ys, probs):
            a, b, c, *_ , f1v, iouv = prf(y, p, t)
            tp += a; fp += b; fn += c
            f1s.append(f1v); ious.append(iouv)
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec  = tp / (tp + fn) if tp + fn else 0.0
        pr[round(float(t), 2)] = (prec, rec)
        if float(np.mean(ious)) > best_iou:
            best_iou, best_t = float(np.mean(ious)), round(float(t), 2)

    # AP = Σ (Rn − Rn−1) × Pn, thresholds descending (recall increasing), R0 = 0
    ap, r_prev = 0.0, 0.0
    for t in sorted(pr, reverse=True):
        _, R = pr[t]
        ap += (R - r_prev) * pr[t][0]
        r_prev = R

    # confusion matrix + mean F1/IoU at the LOCKED threshold
    f1s, ious = [], []
    for y, p in zip(ys, probs):
        tp, fp, fn, tn_extra, *_ , f1v, iouv = prf(y, p, best_t)
        tn = int(((p < best_t) & (y == 0)).sum())
        cm["TP"] += tp; cm["FP"] += fp; cm["FN"] += fn; cm["TN"] += tn
        f1s.append(f1v); ious.append(iouv)

    metrics = {
        "status": "final",
        "f1": round(float(np.mean(f1s)), 4),
        "iou": round(float(np.mean(ious)), 4),
        "mAP": round(float(ap), 4),                    # = AP of the mangrove class
        "threshold": best_t, "split": "80/20",
        "config": {
            "optimizer": "Adam (lr=0.001)",
            "loss": "binary cross-entropy",
            "input": "256×256×5 (B3, B4, B8, B11, NDVI)",
            "output": "sigmoid probability map",
        },
        "pr_curve": {
            "recall":    [pr[t][1] for t in sorted(pr)],
            "precision": [pr[t][0] for t in sorted(pr)],
        },
        "confusion": cm,
    }
    METRICS_OUT.write_text(json.dumps(metrics, indent=2))
    print(f"locked threshold: {best_t:.2f} | F1 {metrics['f1']} | "
          f"IoU {metrics['iou']} | mAP {metrics['mAP']}")
    print(f"wrote {METRICS_OUT}")


if __name__ == "__main__":
    main()
