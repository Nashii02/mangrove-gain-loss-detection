"""
Step 5 — Training (80% train / 20% validation split)

⛔ GATE: do not run until reference masks are MENRO-validated and FROZEN
(thesis: validation precedes training; labels are never modified to improve
performance).  Status: v1 — ported from notebook.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import tensorflow as tf
from config import IMAGES_DIR, MASKS_DIR, MODELS_DIR
from unet_model import build_unet, compile_model

SEED, BATCH, EPOCHS, PATIENCE = 42, 4, 100, 10


def load_pairs():
    pairs = [p for p in sorted(IMAGES_DIR.glob("*.npy"))
             if (MASKS_DIR / p.name).exists()]
    if not pairs:
        raise RuntimeError("No image/mask pairs found — complete labeling first.")
    X = np.stack([np.load(p) for p in pairs]).astype("float32")
    Y = np.stack([np.load(MASKS_DIR / p.name) for p in pairs])[..., None].astype("float32")
    print(f"pairs: {len(pairs)} | X {X.shape} | mangrove fraction {Y.mean():.4f}")
    return X, Y


def main():
    X, Y = load_pairs()
    rng = np.random.default_rng(SEED)
    idx = rng.permutation(len(X))
    split = int(len(X) * 0.8)                                   # thesis: 80/20
    Xtr, Ytr, Xva, Yva = X[idx[:split]], Y[idx[:split]], X[idx[split:]], Y[idx[split:]]
    print(f"train {len(Xtr)} | val {len(Xva)}")

    model = compile_model(build_unet(X.shape[1:]))
    hist = model.fit(
        Xtr, Ytr, validation_data=(Xva, Yva),
        epochs=EPOCHS, batch_size=BATCH,
        callbacks=[tf.keras.callbacks.EarlyStopping(patience=PATIENCE,
                                                    restore_best_weights=True),
                   tf.keras.callbacks.ModelCheckpoint(MODELS_DIR / "best_model.keras",
                                                      save_best_only=True)])
    model.save(MODELS_DIR / "final_model.keras")

    # overfitting check (thesis: monitor train vs. validation loss)
    plt.figure(figsize=(7, 4))
    plt.plot(hist.history["loss"], label="train loss")
    plt.plot(hist.history["val_loss"], label="val loss")
    plt.xlabel("epoch"); plt.ylabel("binary cross-entropy")
    plt.legend(); plt.title("Training vs. validation loss")
    plt.tight_layout()
    plt.savefig(MODELS_DIR / "loss_curve.png", dpi=200)
    print(f"saved: {MODELS_DIR / 'final_model.keras'} + loss_curve.png")


if __name__ == "__main__":
    main()
