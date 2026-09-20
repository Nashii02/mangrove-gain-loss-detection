"""
Step 4 — U-Net architecture
Encoder–decoder CNN with skip connections (Ronneberger et al., 2015), configured
for 5-channel (B3, B4, B8, B11, NDVI) 256×256 input and a single-channel sigmoid
probability output. Matches thesis Fig. 1.  Status: v1 — ported from notebook.
"""
import tensorflow as tf
from tensorflow.keras import layers, Model


def conv_block(x, f):
    """Two 3×3 convolutions with ReLU (per original U-Net design)."""
    x = layers.Conv2D(f, 3, padding="same", activation="relu")(x)
    x = layers.Conv2D(f, 3, padding="same", activation="relu")(x)
    return x


def build_unet(input_shape=(256, 256, 5)):
    inp = layers.Input(input_shape)

    # ── Encoder (contracting path) ──
    s1 = conv_block(inp, 64);  p1 = layers.MaxPooling2D()(s1)
    s2 = conv_block(p1, 128);  p2 = layers.MaxPooling2D()(s2)
    s3 = conv_block(p2, 256);  p3 = layers.MaxPooling2D()(s3)
    s4 = conv_block(p3, 512);  p4 = layers.MaxPooling2D()(s4)

    # ── Bottleneck ──
    b = conv_block(p4, 1024)

    # ── Decoder (expanding path) + skip connections ──
    u4 = layers.Conv2DTranspose(512, 2, strides=2, padding="same")(b)
    d4 = conv_block(layers.concatenate([u4, s4]), 512)
    u3 = layers.Conv2DTranspose(256, 2, strides=2, padding="same")(d4)
    d3 = conv_block(layers.concatenate([u3, s3]), 256)
    u2 = layers.Conv2DTranspose(128, 2, strides=2, padding="same")(d3)
    d2 = conv_block(layers.concatenate([u2, s2]), 128)
    u1 = layers.Conv2DTranspose(64, 2, strides=2, padding="same")(d2)
    d1 = conv_block(layers.concatenate([u1, s1]), 64)

    # ── Output: sigmoid probability map 256×256×1 ──
    out = layers.Conv2D(1, 1, activation="sigmoid")(d1)
    return Model(inp, out, name="unet_mangrove")


def compile_model(model, lr=0.001):
    """Thesis spec: Adam optimizer, learning rate 0.001, binary cross-entropy loss."""
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
                  loss="binary_crossentropy")
    return model


if __name__ == "__main__":
    m = compile_model(build_unet())
    m.summary()
