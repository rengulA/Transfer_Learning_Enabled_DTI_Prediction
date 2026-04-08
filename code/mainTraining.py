import argparse
import os
from feedForwardDNNDTIFiveFold import training_test

parser = argparse.ArgumentParser(description='feedForwardDNN arguments')

parser.add_argument(
    '--chln',
    type=str,
    default="1200_300",
    metavar='HLN',
    help='number of neurons in hidden layers of compound(default: 1200_100)')

parser.add_argument(
    '--lr',
    type=float,
    default=0.0001,
    metavar='LR',
    help='learning rate (default: 0.002)')

parser.add_argument(
    '--bs',
    type=int,
    default=256,
    metavar='BS',
    help='batch size (default: 256)')

parser.add_argument(
    '--td',
    type=str,
    default="MTHFD2",
    metavar='TD',
    help='the name of the target dataset (default: MTHFD2)')

parser.add_argument(
    '--sd',
    type=str,
    default="MTHFD2_source",
    metavar='SD',
    help='the name of the source dataset (default: MTHFD2_source)')

parser.add_argument(
    '--do',
    type=float,
    default=0.1,
    metavar='DO',
    help='dropout rate (default: 0.1)')

parser.add_argument(
    '--en',
    type=str,
    default="my_experiments",
    metavar='EN',
    help='the name of the experiment (default: my_experiment)')

parser.add_argument(
    '--model',
    type=str,
    default="fc_2_layer",
    metavar='mn',
    help='model name (default: fc_2_layer)')

parser.add_argument(
    '--epoch',
    type=int,
    default=100,
    metavar='EPOCH',
    help='Number of epochs (default: 100)')

parser.add_argument(
    '--sf',
    type=int,
    default=0,
    metavar='SF',
    help='subset flag (default: 0)')

parser.add_argument(
    '--tlf',
    type=int,
    default=0,
    metavar='TLF',
    help='transfer learning flag (default: 0)')

parser.add_argument(
    '--ff',
    type=int,
    default=0,
    metavar='FF',
    help='freeze flag (default: 0)')

parser.add_argument(
    '--fl',
    type=str,
    default="1",
    metavar='FL',
    help='hidden layers to be frozen (default: 1)')

parser.add_argument(
    '--el',
    type=str,
    default="1",
    metavar='EL',
    help='layer to be extracted (default: 0)')

parser.add_argument(
    '--ss',
    type=int,
    default=10,
    metavar='SS',
    help='subset size (default: 10)')

parser.add_argument(
    '--cf',
    type=str,
    default="chemprop",
    metavar='CF',
    help='compound features separated by underscore character (default: ecfp4)')

parser.add_argument(
    '--et',
    type=str,
    default="-",
    metavar='ET',
    help='external test dataset (default: -)')

parser.add_argument(
    '--ip',
    type=str,
    default=os.getcwd(),
    metavar='IP',
    help='input path (default: current working directory)')

parser.add_argument(
    '--op',
    type=str,
    default=os.getcwd(),
    metavar='OP',
    help='output path (default: current working directory)')

parser.add_argument(
    '--nc',
    type=int,
    default=2,
    metavar='NC',
    help='number of result classes (default: 2)')

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    comp_hidden_layer_neurons = [int(num) for num in args.chln.split("_")]


    training_test(args.td, args.sd, args.cf.split("-"), comp_hidden_layer_neurons, args.lr, args.bs,
                      args.model, args.do, args.en, args.epoch, args.sf, args.tlf, args.ff, args.fl, args.ss,
                      args.ip, args.op, args.nc)
       
    
        
