
No Animation on some saved data:
python main.py --input_type synthetic_data/regular_6.txt --delta 1.0 --rho 0.5 --animation 0
python main.py --input_type synthetic_data/star.txt --delta 1.0 --rho 0.5 --animation 0
python main.py --input_type synthetic_data/snake.txt --delta 1.0 --rho 0.5 --animation 0
python main.py --input_type synthetic_data/regular_10.txt --delta 1.0 --rho 0.5 --animation 0

No animation with mouse input:
python main.py --input_type stdin --delta 1.0 --rho 0.5 --animation 0

Animation on some saved data:
python main.py --input_type synthetic_data/regular_6.txt --delta 1.0 --rho 1.0 --animation 1
python main.py --input_type synthetic_data/star.txt --delta 1.0 --rho 1.0 --animation 1
python main.py --input_type synthetic_data/snake.txt --delta 1.0 --rho 1.0 --animation 1
python main.py --input_type synthetic_data/regular_10.txt --delta 1.0 --rho 1.0 --animation 1

Animation with mouse input:

python main.py --input_type stdin --delta 1.0 --rho 1.0 --animation 1

Some Real data:

python main.py --input_type nyc_data/example_00000 --delta 1.0 --rho 1.0 --animation 0
python main.py --input_type nyc_data/example_00004 --delta 1.0 --rho 1.0 --animation 0
python main.py --input_type nyc_data/example_00005 --delta 1.0 --rho 1.0 --animation 0
python main.py --input_type nyc_data/example_03248 --delta 1.0 --rho 1.0 --animation 0
python main.py --input_type nyc_data/example_02222 --delta 1.0 --rho 1.0 --animation 0

