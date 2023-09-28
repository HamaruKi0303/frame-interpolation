#!/bin/bash

python3 -m eval.interpolator_cli --pattern "$1" --model_path pretrained_models/film_net/Style/saved_model --output_video --times_to_interpolate "$2" --fps "$3"