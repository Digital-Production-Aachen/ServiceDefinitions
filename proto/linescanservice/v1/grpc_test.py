from absl import app
from absl import flags
from absl import logging
from absl.testing import absltest
from absl.testing import flagsaver

from proto.linescannerservice import linescanservice_pb2
from proto.linescannerservice import linescanservice_pb2_grpc
from proto.axesservice import axescontroller_pb2
from proto.axesservice import axescontroller_pb2_grpc

import grpc
import os
import sys
import _thread
import time 

import random
from matplotlib import pyplot as plt
import numpy as np
import scipy.misc
import time

FLAGS = flags.FLAGS
flags.DEFINE_string(
    'hostLinescan', '0.0.0.0:50053', 'The hostLinescan the GRPC test should run against'
)

possible_resolutions = [256, 512, 1024, 2048]
exp_max = 4095


class TestLinescannerservice(absltest.TestCase):
    
    def setUp(self):
    
        # -- gprc channel to scanner
        self.channel_linescan = grpc.insecure_channel(FLAGS.hostLinescan)
        self.stub_linescan  = linescanservice_pb2_grpc.LinescanControlStub(self.channel_linescan) 
        
 
    def stop(self):
        self.channel_linescan.close()


    def test_scan_internal_trigger_correct(self):
        for res in possible_resolutions:
            exp = round(random.randint(1, exp_max), 2)
            response = self.stub_linescan.ScanWithInternalTrigger(linescanservice_pb2.DeviceParams(resolution=res, exposure=exp))
        self.assertEqual(len(response.x), res)
        self.assertEqual(len(response.z), res)
   

    def test_scan_internal_trigger_error(self):
        
        for n in range(5):
       
            res = random.randint(0, 100000)
            exp = round(random.randint(1, exp_max), 2)
            
            with self.assertRaises(grpc.RpcError) as cm:
                self.stub_linescan.ScanWithInternalTrigger(linescanservice_pb2.DeviceParams(resolution=res, exposure=exp))
                self.assertEqual(cm.exception.code(), grpc.StatusCode.INVALID_ARGUMENT)       
  

if __name__ == "__main__":
    absltest.main()

