# this script runs a model through training, testing and prediction of all datasets

# profiling with tree visualization
# pip install snakeviz
# https://jiffyclub.github.io/snakeviz/
# python -m cProfile -o poco.prof poco.py
# snakeviz poco.prof

import os

python_call = 'python'
main_cmd = 'poco.py'
name = 'poco'
version = '0'
on_server = False

debug = ''
print_config = ''

# uncomment for debugging
# debug += '--debug True'
# print_config += '--print_config'

# python_call += ' -m cProfile -o poco.prof'  # uncomment for profiling

main_cmd = python_call + ' ' + main_cmd

cmd_template = '{main_cmd} {sub_cmd} {configs} {debug} {print_config}'
configs = '{server} -c configs/{name}.yaml'

# training
configs_train = configs.format(server='-c configs/device_server.yaml' if on_server else '', name=name)
cmd_train = cmd_template.format(main_cmd=main_cmd, sub_cmd='fit', configs=configs_train, debug=debug, print_config=print_config)
cmd_train += ' --data.init_args.in_file datasets/abc_train/trainset.txt'
os.system(cmd_train)

args_no_train = (
    '--ckpt_path models/{name}/version_{version}/checkpoints/last.ckpt '
    '--trainer.logger False '  # comment for profiling
    '--trainer.devices 1'
).format(name=name, version=version)
configs_no_train = configs.format(server='', name=name)
cmd_template_no_train = cmd_template + ' --data.init_args.in_file {dataset}/testset.txt ' + args_no_train

# testing
cmd_test = cmd_template_no_train.format(main_cmd=main_cmd, sub_cmd='test', configs=configs_no_train, 
                                        dataset='datasets/abc', debug=debug, print_config=print_config)
os.system(cmd_test)

# prediction
datasets = [
    'abc_minimal',
    # 'abc',
    # 'abc_extra_noisy',
    # 'abc_noisefree',
    # 'real_world',
    # 'famous_original', 'famous_noisefree', 'famous_sparse', 'famous_dense', 'famous_extra_noisy',
    # 'thingi10k_scans_original', 'thingi10k_scans_noisefree', 'thingi10k_scans_sparse',
    # 'thingi10k_scans_dense', 'thingi10k_scans_extra_noisy'
    ]
for ds in datasets:
    cmd_pred = cmd_template_no_train.format(main_cmd=main_cmd, sub_cmd='predict', configs=configs_no_train, 
                                            dataset='datasets/' + ds, debug=debug, print_config=print_config)
    # cmd_pred += ' -c configs/profiler.yaml'
    # cmd_pred += ' --model.init_args.gen_resolution_global 129'
    os.system(cmd_pred)
