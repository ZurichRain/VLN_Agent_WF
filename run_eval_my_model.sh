name=VLNBERT-train-Prevalent

flag="--vlnbert prevalent

      --aug data/R2R/prevalent_aug.json
      --test_only 0

      --train auglistener

      --features places365
      --maxAction 15
      --batchSize 1
      --feedback sample
      --lr 1e-5
      --iters 300000
      --optim adamW

      --mlWeight 0.20
      --maxInput 80
      --angleFeatSize 128
      --featdropout 0.4
      --dropout 0.5"

mkdir -p snap/$name
CUDA_VISIBLE_DEVICES=0 python3 get_eval_my_model.py $flag --name $name