import grpc
import os
from proto.scannerservice import scannerservice_pb2_grpc
from proto.scannerservice import scannerservice_pb2
from proto.laservectorformat import laservectorformat_pb2
from absl import app
from absl import flags
from absl.testing import absltest
from absl.testing import flagsaver

FLAGS = flags.FLAGS

flags.DEFINE_string('host', '127.0.0.1:50051', 'The host the GRPC test should run against')

class TestScannerServer(absltest.TestCase):

    def setUp(self):
        self.channel = grpc.insecure_channel(FLAGS.host)
        self.stub = scannerservice_pb2_grpc.HardwareControllerStub(self.channel)

    def test_smoke_jump_to_pos(self):
        pos = scannerservice_pb2.Position()
        self.stub.JumpToPosition(pos)

    def test_smoke_get_hard_scan_field(self):
        self.stub.GetHardScanField(scannerservice_pb2.Empty())

    def test_smoke_scan_layer(self):
        try:
            self.stub.ScanLayer(scannerservice_pb2.LayerMessage())
        except grpc.RpcError as e:
            self.assertTrue(e.code()==grpc.StatusCode.INVALID_ARGUMENT)
            return
        # Break if not Statuscode got returned because an empty Layermessage has to fail
        self.fail("GRPC Call did not fail")

    def test_jump_to_pos(self):
        config = self.stub.GetHardScanField(scannerservice_pb2.Empty())
        # Test if edges are included
        pos = scannerservice_pb2.Position(x = config.xminimum,y = config.yminimum)
        self.stub.JumpToPosition(pos)
        pos = scannerservice_pb2.Position(x = config.xmaximum,y = config.yminimum)
        self.stub.JumpToPosition(pos)
        pos = scannerservice_pb2.Position(x = config.xmaximum,y = config.ymaximum)
        self.stub.JumpToPosition(pos)
        pos = scannerservice_pb2.Position(x = config.xminimum,y = config.ymaximum)
        self.stub.JumpToPosition(pos)

        # Test zeros
        pos = scannerservice_pb2.Position()
        self.stub.JumpToPosition(pos)

    def test_jump_to_pos_error(self):
        config = self.stub.GetHardScanField(scannerservice_pb2.Empty())

        # min / min
        pos = scannerservice_pb2.Position(x = config.xminimum-1,y = config.yminimum)
        with self.assertRaises(grpc.RpcError):
            self.stub.JumpToPosition(pos)

        pos = scannerservice_pb2.Position(x = config.xminimum,y = config.yminimum-1)
        with self.assertRaises(grpc.RpcError):
            self.stub.JumpToPosition(pos)

        pos = scannerservice_pb2.Position(x = config.xminimum-1,y = config.yminimum-1)
        with self.assertRaises(grpc.RpcError):
            self.stub.JumpToPosition(pos)
        
        # max / min

        pos = scannerservice_pb2.Position(x = config.xmaximum+1,y = config.yminimum)
        with self.assertRaises(grpc.RpcError):
            self.stub.JumpToPosition(pos)

        pos = scannerservice_pb2.Position(x = config.xmaximum+1,y = config.yminimum-1)
        with self.assertRaises(grpc.RpcError):
            self.stub.JumpToPosition(pos)

        pos = scannerservice_pb2.Position(x = config.xmaximum,y = config.yminimum-1)
        with self.assertRaises(grpc.RpcError):
            self.stub.JumpToPosition(pos)

        # min / max

        pos = scannerservice_pb2.Position(x = config.xminimum-1,y = config.ymaximum)
        with self.assertRaises(grpc.RpcError):
            self.stub.JumpToPosition(pos)

        pos = scannerservice_pb2.Position(x = config.xminimum-1,y = config.ymaximum + 1)
        with self.assertRaises(grpc.RpcError):
            self.stub.JumpToPosition(pos)

        pos = scannerservice_pb2.Position(x = config.xminimum,y = config.ymaximum + 1)
        with self.assertRaises(grpc.RpcError):
            self.stub.JumpToPosition(pos)

        # max / max
        pos = scannerservice_pb2.Position(x = config.xmaximum+1,y = config.ymaximum)
        with self.assertRaises(grpc.RpcError):
            self.stub.JumpToPosition(pos)

        pos = scannerservice_pb2.Position(x = config.xmaximum+1,y = config.ymaximum+1)
        with self.assertRaises(grpc.RpcError):
            self.stub.JumpToPosition(pos)

        pos = scannerservice_pb2.Position(x = config.xmaximum,y = config.ymaximum+1)
        with self.assertRaises(grpc.RpcError):
            self.stub.JumpToPosition(pos)

    def test_scan_line(self):
        config = self.stub.GetHardScanField(scannerservice_pb2.Empty())
        layer = laservectorformat_pb2.Layer()

        #create square
        lines = laservectorformat_pb2.VectorBlock.LineSequence()
        lines.points.append(0)
        lines.points.append(0)

        lines.points.append(config.xminimum)
        lines.points.append(config.yminimum)

        lines.points.append(config.xmaximum)
        lines.points.append(config.yminimum)

        lines.points.append(config.xmaximum)
        lines.points.append(config.ymaximum)

        lines.points.append(config.xminimum)
        lines.points.append(config.ymaximum)

        vectorblock = laservectorformat_pb2.VectorBlock(markingParamsKey=0,lineSequence = lines)
        params = laservectorformat_pb2.MarkingParams(
                                            jumpSpeedInMmS=2000,
                                            laserSpeedInMmS=2000)

        layer.vectorBlocks.append(vectorblock)
        message = scannerservice_pb2.LayerMessage(layer = layer, markingparams=[params])
        a = self.stub.ScanLayer(message)

    def test_scan_line_wrong_number_of_points(self):
        config = self.stub.GetHardScanField(scannerservice_pb2.Empty())
        layer = laservectorformat_pb2.Layer()
        lines = laservectorformat_pb2.VectorBlock.LineSequence()
        lines.points.append(0)
        vectorblock = laservectorformat_pb2.VectorBlock(markingParamsKey=0,lineSequence = lines)
        params = laservectorformat_pb2.MarkingParams(
                                            jumpSpeedInMmS=2000,
                                            laserSpeedInMmS=2000)
        layer.vectorBlocks.append(vectorblock)
        message = scannerservice_pb2.LayerMessage(layer = layer, markingparams=[params])
        with self.assertRaises(grpc.RpcError) as cm:
            self.stub.ScanLayer(message)
        self.assertTrue(cm.exception.code()==grpc.StatusCode.INVALID_ARGUMENT)

    def test_scan_line_points_out_of_range(self):
        config = self.stub.GetHardScanField(scannerservice_pb2.Empty())
        tested_lines=[[0 , config.ymaximum+1],
                      [config.xmaximum+1 , 0],
                      [0 , config.yminimum-1],
                      [config.xminimum-1 , 0]]
        for i in tested_lines:
            layer = laservectorformat_pb2.Layer()
            lines = laservectorformat_pb2.VectorBlock.LineSequence()

            lines.points.append(0)
            lines.points.append(0)
            lines.points.append(i[0])
            lines.points.append(i[1])

            vectorblock = laservectorformat_pb2.VectorBlock(markingParamsKey=0,lineSequence = lines)
            params = laservectorformat_pb2.MarkingParams(
                                            jumpSpeedInMmS=2000,
                                            laserSpeedInMmS=2000)
            layer.vectorBlocks.append(vectorblock)
            message = scannerservice_pb2.LayerMessage(layer = layer, markingparams=[params])
            with self.assertRaises(grpc.RpcError) as cm:
                self.stub.ScanLayer(message)
            self.assertTrue(cm.exception.code()==grpc.StatusCode.INVALID_ARGUMENT)
    def test_scan_hatches(self):
        config = self.stub.GetHardScanField(scannerservice_pb2.Empty())
        layer = laservectorformat_pb2.Layer()

        #create square
        hatches = laservectorformat_pb2.VectorBlock.Hatches()

        hatches.points.append(config.xminimum)
        hatches.points.append(config.yminimum)

        hatches.points.append(config.xmaximum)
        hatches.points.append(config.yminimum)

        hatches.points.append(config.xmaximum)
        hatches.points.append(config.ymaximum)

        hatches.points.append(config.xminimum)
        hatches.points.append(config.ymaximum)

        vectorblock = laservectorformat_pb2.VectorBlock(markingParamsKey=0,hatches = hatches)
        params = laservectorformat_pb2.MarkingParams(
                                            jumpSpeedInMmS=2000,
                                            laserSpeedInMmS=2000)

        layer.vectorBlocks.append(vectorblock)
        message = scannerservice_pb2.LayerMessage(layer = layer, markingparams=[params])
        a = self.stub.ScanLayer(message)

    def test_scan_hatches_wrong_number_of_points(self):
        config = self.stub.GetHardScanField(scannerservice_pb2.Empty())
        for i in range(1,3):
            layer = laservectorformat_pb2.Layer()
            hatches = laservectorformat_pb2.VectorBlock.Hatches()
            for j in range(i):
                hatches.points.append(0)
            vectorblock = laservectorformat_pb2.VectorBlock(markingParamsKey=0,hatches = hatches)
            params = laservectorformat_pb2.MarkingParams(
                                                jumpSpeedInMmS=2000,
                                                laserSpeedInMmS=2000)
            layer.vectorBlocks.append(vectorblock)
            message = scannerservice_pb2.LayerMessage(layer = layer, markingparams=[params])
            with self.assertRaises(grpc.RpcError) as cm:
                self.stub.ScanLayer(message)
            self.assertTrue(cm.exception.code()==grpc.StatusCode.INVALID_ARGUMENT)

    def test_scan_hatches_out_of_range(self):
        config = self.stub.GetHardScanField(scannerservice_pb2.Empty())
        test_dot = [[ config.xminimum - 1 , 0 ],
                    [0 , config.yminimum - 1],
                    [config.xminimum - 1 , config.yminimum - 1],
                    [config.xmaximum + 1 , 0],
                    [0 , config.ymaximum + 1],
                    [config.xmaximum + 1 , config.ymaximum + 1]]

        for i in test_dot:
            layer = laservectorformat_pb2.Layer()
            hatches = laservectorformat_pb2.VectorBlock.Hatches()

            hatches.points.append(0)
            hatches.points.append(0)
            hatches.points.append(i[0])
            hatches.points.append(i[1])

            vectorblock = laservectorformat_pb2.VectorBlock(markingParamsKey=0,hatches = hatches)
            params = laservectorformat_pb2.MarkingParams(
                                                jumpSpeedInMmS=2000,
                                                laserSpeedInMmS=2000)
            layer.vectorBlocks.append(vectorblock)
            message = scannerservice_pb2.LayerMessage(layer = layer, markingparams=[params])
            with self.assertRaises(grpc.RpcError) as cm:
                self.stub.ScanLayer(message)
            self.assertTrue(cm.exception.code()==grpc.StatusCode.INVALID_ARGUMENT)


    def tearDown(self):
        self.channel.close()
        

if __name__ == "__main__":
    absltest.main()

