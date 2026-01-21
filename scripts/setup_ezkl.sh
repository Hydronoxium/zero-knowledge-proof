#!/bin/bash
set -e

python create_big_model.py

ezkl gen-settings -M big_model.onnx
ezkl compile-circuit -M big_model.onnx

mv model.compiled compiled_reference.ezkl

ezkl gen-srs --srs-path ~/.ezkl/srs/kzg17.srs --logrows 17

ezkl setup --compiled-circuit compiled_reference.ezkl

mv pk.key pk_reference.key
mv vk.key vk_reference.key

cp pk_reference.key pk.key
cp vk_reference.key vk.key

echo "Setup complete."
