# from abc import ABC
# # import torch
# # import torch.nn as nn
# from typing import Union, Sequence
#
#
# class MLP(nn.Module, ABC):
#     def __init__(
#             self, in_dim: int, dims: Sequence[int]
#     ):
#         self.in_dim = in_dim
#         self.out_dim = dims[-1]
#         super(MLP, self).__init__()
#         all_dims = [in_dim, *dims]
#         layers = []
#
#         for i, (in_dim, out_dim) in enumerate(zip(all_dims[:-1], all_dims[1:])):
#             layers += [
#                 nn.Dropout(p=0.5),
#                 nn.Linear(in_dim, out_dim, bias=True),
#                 nn.ReLU()
#                 # nn.Sigmoid()
#
#             ]
#
#         # self.fc_layers = nn.Sequential(*layers[:-2])
#         self.fc_layers = nn.Sequential(*layers[:-3], layers[-2])
#
#     def forward(self, x: torch.Tensor) -> torch.Tensor:
#         # print(f'{x.shape=}, {self.in_dim=}')
#         assert x.shape[1] == self.in_dim
#         x = torch.reshape(x, (x.shape[0], -1))
#         y_pred = self.fc_layers(x)
#         assert y_pred.shape[1] == self.out_dim
#         return y_pred
#
#
# class CNN(nn.Module, ABC):
#     def __init__(self, in_size, in_channels=1, directions_num=100, hidden_dims=[100]):
#         super().__init__()
#         self.in_size = in_size
#         self.in_channels = in_channels
#         self.out_classes = directions_num
#         self.hidden_dims = hidden_dims
#         self.feature_extractor = self._make_feature_extractor_2D()
#         # self.feature_extractor = self.mnist_feature_extractor()
#         self.mlp = self._make_mlp()
#
#     def _make_feature_extractor_1(self):
#         seq = nn.Sequential(
#             nn.Conv3d(self.in_channels, out_channels=32, kernel_size=5, padding=(2, 0, 0)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             nn.Conv3d(in_channels=32, out_channels=32, kernel_size=5, padding=(2, 0, 0)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             nn.Conv3d(in_channels=32, out_channels=32, kernel_size=5, dilation=(1, 2, 2), padding=(2, 0, 0)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             nn.Conv3d(in_channels=32, out_channels=32, kernel_size=5, dilation=(1, 4, 4), padding=(2, 0, 0)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             # nn.MaxPool3d(kernel_size=3, padding=(1, 0, 0)),
#             nn.Conv3d(in_channels=32, out_channels=64, kernel_size=(3, 5, 5)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(64),
#             nn.Conv3d(in_channels=64, out_channels=64, kernel_size=1),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(64),
#             nn.Conv3d(in_channels=128, out_channels=self.out_classes, kernel_size=1),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(self.out_classes)
#         )
#         seq.eval()
#         return seq
#
#     def _make_feature_extractor_2(self):
#         seq = nn.Sequential(
#             nn.Conv3d(self.in_channels, out_channels=16, kernel_size=3),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(16),
#             # 30
#             nn.Conv3d(in_channels=16, out_channels=16, kernel_size=3),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(16),
#             # 28
#             nn.Conv3d(in_channels=16, out_channels=32, kernel_size=3),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             # 26
#             nn.Conv3d(in_channels=32, out_channels=32, kernel_size=3),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             # 24
#             nn.Conv3d(in_channels=32, out_channels=64, kernel_size=3),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(64),
#             # 22
#             nn.Conv3d(in_channels=64, out_channels=64, kernel_size=3),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(64),
#             # 20
#             nn.Conv3d(in_channels=64, out_channels=64, kernel_size=3),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(64),
#             # 18
#             nn.Conv3d(in_channels=64, out_channels=128, kernel_size=3),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(128),
#             # 16
#             nn.Conv3d(in_channels=128, out_channels=128, kernel_size=3),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(128),
#             # 14
#             nn.Conv3d(in_channels=128, out_channels=128, kernel_size=3),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(128),
#             # 12
#             nn.Conv3d(in_channels=128, out_channels=128, kernel_size=3),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(128),
#             # 10
#             nn.Conv3d(in_channels=128, out_channels=256, kernel_size=3),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(256),
#             # 8
#             nn.Conv3d(in_channels=256, out_channels=256, kernel_size=3),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(256),
#             # 6
#             nn.Conv3d(in_channels=256, out_channels=256, kernel_size=3),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(256),
#             # 4
#             nn.Conv3d(in_channels=256, out_channels=256, kernel_size=3),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(256),
#             # 2
#             nn.Conv3d(in_channels=256, out_channels=256, kernel_size=2),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(256),
#             # 1
#             nn.Conv3d(in_channels=256, out_channels=128, kernel_size=1),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(128),
#             # 3
#             nn.Conv3d(in_channels=128, out_channels=self.out_classes, kernel_size=1),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(self.out_classes)
#         )
#         seq.eval()
#         return seq
#
#     def _make_feature_extractor_3(self):
#         seq = nn.Sequential(
#             nn.Conv3d(self.in_channels, out_channels=32, kernel_size=(3, 3, 3)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             nn.Conv3d(in_channels=32, out_channels=32, kernel_size=(3, 3, 3)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             # nn.Dropout(p=0.5),
#             nn.Conv3d(in_channels=32, out_channels=32, kernel_size=(3, 3, 3), dilation=(2, 2, 2)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             nn.Conv3d(in_channels=32, out_channels=32, kernel_size=(3, 3, 3), dilation=(2, 2, 2)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             # nn.Dropout(p=0.5),
#             nn.Conv3d(in_channels=32, out_channels=32, kernel_size=(3, 3, 3), dilation=(4, 4, 4)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             nn.Conv3d(in_channels=32, out_channels=32, kernel_size=(3, 3, 3), dilation=(4, 4, 4)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             # nn.Dropout(p=0.5),
#             nn.Conv3d(in_channels=32, out_channels=64, kernel_size=(3, 3, 3)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(64),
#             # nn.Dropout(p=0.5),
#             nn.Conv3d(in_channels=64, out_channels=64, kernel_size=(2, 2, 2)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(64),
#             # nn.Dropout(p=0.5),
#             nn.Conv3d(in_channels=64, out_channels=self.out_classes, kernel_size=1),
#             # nn.ReLU(inplace=True),
#             # nn.BatchNorm3d(self.out_classes)
#         )
#         seq.eval()
#         return seq
#
#     def _make_feature_extractor_4(self):
#         seq = nn.Sequential(
#             nn.Conv3d(self.in_channels, out_channels=32, kernel_size=(3, 3, 3)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             nn.Conv3d(in_channels=32, out_channels=32, kernel_size=(3, 3, 3)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             # nn.Dropout(p=0.5),
#             nn.Conv3d(in_channels=32, out_channels=32, kernel_size=(3, 3, 3), dilation=(2, 2, 2)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             nn.Conv3d(in_channels=32, out_channels=32, kernel_size=(3, 3, 3), dilation=(2, 2, 2)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             # nn.Dropout(p=0.5),
#             nn.Conv3d(in_channels=32, out_channels=64, kernel_size=(3, 3, 3)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(64),
#             # nn.Dropout(p=0.5),
#             nn.Conv3d(in_channels=64, out_channels=64, kernel_size=(2, 2, 2)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(64),
#             # nn.Dropout(p=0.5),
#             nn.Conv3d(in_channels=64, out_channels=self.out_classes, kernel_size=1),
#             # nn.ReLU(inplace=True),
#             # nn.BatchNorm3d(self.out_classes)
#         )
#         seq.eval()
#         return seq
#
#     def _make_feature_extractor_5(self):
#         seq = nn.Sequential(
#             nn.Conv3d(self.in_channels, out_channels=32, kernel_size=(3, 3, 3)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             nn.MaxPool3d(kernel_size=2),
#             nn.Dropout3d(p=0.1),
#             nn.Conv3d(in_channels=32, out_channels=64, kernel_size=(3, 3, 3)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(64),
#             nn.MaxPool3d(kernel_size=2),
#             nn.Dropout3d(p=0.1),
#             nn.Conv3d(in_channels=64, out_channels=64, kernel_size=(3, 3, 3)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(64),
#             nn.Dropout3d(p=0.2)
#             # nn.Conv3d(in_channels=32, out_channels=64, kernel_size=(3, 3, 3)),
#             # nn.ReLU(inplace=True),
#             # nn.BatchNorm3d(64),
#             # nn.Dropout3d(p=0.5),
#             # nn.Conv3d(in_channels=64, out_channels=64, kernel_size=(3, 3, 3)),
#             # nn.ReLU(inplace=True),
#             # nn.BatchNorm3d(64),
#             # nn.Dropout3d(p=0.5),
#             # nn.Conv3d(in_channels=64, out_channels=32, kernel_size=(3, 3, 3)),
#             # nn.ReLU(inplace=True),
#             # nn.BatchNorm3d(32),
#             # nn.Conv3d(in_channels=32, out_channels=2, kernel_size=(1, 1, 1))
#             # nn.MaxPool3d(kernel_size=3)
#         )
#         seq.eval()
#         return seq
#
#     def _make_feature_extractor_6(self):
#         seq = nn.Sequential(
#             nn.Conv3d(self.in_channels, out_channels=32, kernel_size=(3, 3, 3)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             nn.Conv3d(in_channels=32, out_channels=32, kernel_size=(3, 3, 3)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             nn.MaxPool3d(kernel_size=2),
#             nn.Dropout3d(p=0.1),
#             nn.Conv3d(in_channels=32, out_channels=32, kernel_size=(3, 3, 3), dilation=(2, 2, 2)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             nn.Dropout3d(p=0.1),
#             nn.Conv3d(in_channels=32, out_channels=32, kernel_size=(3, 3, 3), dilation=(4, 4, 4)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(32),
#             nn.Dropout3d(p=0.1),
#             nn.Conv3d(in_channels=32, out_channels=64, kernel_size=(2, 2, 2)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(64),
#             nn.Dropout3d(p=0.1),
#             nn.Conv3d(in_channels=64, out_channels=64, kernel_size=(1, 1, 1)),
#             nn.ReLU(inplace=True),
#             nn.BatchNorm3d(64),
#             nn.Dropout3d(p=0.1)
#             # nn.Conv3d(in_channels=64, out_channels=2, kernel_size=(1, 1, 1)),
#             # nn.ReLU(inplace=True),
#             # nn.BatchNorm3d(2),
#             # nn.Dropout3d(p=0.1)
#         )
#         seq.eval()
#         return seq
#
#     def _make_feature_extractor_7(self):
#         seq = nn.Sequential(
#             nn.Conv3d(self.in_channels, out_channels=16, kernel_size=(1, 3, 3)),
#             nn.BatchNorm3d(16),
#             nn.ReLU(),
#             nn.MaxPool3d(kernel_size=(1, 2, 2)),
#             nn.Conv3d(in_channels=16, out_channels=32, kernel_size=(1, 3, 3)),
#             nn.BatchNorm3d(32),
#             nn.ReLU(),
#             nn.MaxPool3d(kernel_size=(1, 2, 2)),
#             nn.Conv3d(in_channels=32, out_channels=64, kernel_size=(3, 3, 3)),
#             nn.BatchNorm3d(64),
#             nn.ReLU(),
#             nn.MaxPool3d(kernel_size=(1, 2, 2))
#         )
#         seq.eval()
#         return seq
#
#     def LeNet5(self):
#         seq = nn.Sequential(
#             nn.Conv3d(self.in_channels, out_channels=32, kernel_size=(5, 5, 5)),
#             nn.Sigmoid(),
#             nn.AvgPool3d(kernel_size=2),
#             nn.Conv3d(in_channels=32, out_channels=32, kernel_size=(5, 5, 5)),
#             nn.Sigmoid(),
#             nn.AvgPool3d(kernel_size=2),
#             nn.Dropout3d(p=0.5)
#         )
#         seq.eval()
#         return seq
#
#     def mnist_feature_extractor(self):
#         seq = nn.Sequential(
#             nn.Conv2d(self.in_channels, out_channels=16, kernel_size=(3, 3)),
#             nn.BatchNorm2d(16),
#             nn.ReLU(),
#             nn.MaxPool2d(kernel_size=2),
#             nn.Conv2d(in_channels=16, out_channels=32, kernel_size=(3, 3)),
#             nn.BatchNorm2d(32),
#             nn.ReLU(),
#             nn.MaxPool2d(kernel_size=2),
#             nn.Conv2d(in_channels=32, out_channels=64, kernel_size=(3, 3)),
#             nn.BatchNorm2d(64),
#             nn.ReLU(),
#             nn.MaxPool2d(kernel_size=2)
#         )
#         seq.eval()
#         return seq
#
#     def _make_feature_extractor_2D(self):
#         seq = nn.Sequential(
#             nn.Conv2d(self.in_channels, out_channels=16, kernel_size=(3, 3)),
#             nn.BatchNorm2d(16),
#             nn.ReLU(),
#             nn.MaxPool2d(kernel_size=2),
#             nn.Conv2d(in_channels=16, out_channels=32, kernel_size=(3, 3)),
#             nn.BatchNorm2d(32),
#             nn.ReLU(),
#             nn.MaxPool2d(kernel_size=2),
#             nn.Conv2d(in_channels=32, out_channels=64, kernel_size=(3, 3)),
#             nn.BatchNorm2d(64),
#             nn.ReLU(),
#             nn.MaxPool2d(kernel_size=2)
#         )
#         seq.eval()
#         return seq
#
#     def _n_features(self) -> int:
#         rng_state = torch.get_rng_state()
#         try:
#             test_image = torch.randint(low=0, high=256, size=self.in_size, dtype=torch.float).unsqueeze(0)
#             test_image = test_image.unsqueeze(0)
#
#             # test_image0 = test_image[:, :, 0, :, :]
#
#             test_out = self.feature_extractor(test_image)
#             C = test_out.shape[1]
#             D = test_out.shape[2]
#             H = test_out.shape[3]
#             # W = test_out.shape[4]
#             # print(C, D, H, W)
#             # return C * D * H * W
#             return C * D * H
#         finally:
#             torch.set_rng_state(rng_state)
#
#     def _make_mlp(self):
#         in_dim = self._n_features()  # in_dim = 73926
#         # print("in_dim = ", in_dim)
#         mlp = MLP(
#             in_dim=in_dim,
#             dims=self.hidden_dims
#         )
#         # output_layer = nn.Linear(self.hidden_dims[-1], self.out_classes, bias=True)
#         # mlp = nn.Sequential(mlp, output_layer)
#         mlp = nn.Sequential(mlp)
#         return mlp
#
#     def forward(self, x):
#         x = torch.unsqueeze(x, 1)
#         # print(f'Net: {x.size()=}')
#         features = self.feature_extractor(x)
#         # print(f'Net: {features.size()=}')
#         features = features.view(features.size(0), -1)
#         # print(f'Net: after view {features.size()=}')
#         class_scores = self.mlp(features)
#         return class_scores
#
#         # print(f'forward: x shape: {x.shape}')
#         # x0 = x[:, :, 0, :, :]
#         # features_0 = self.feature_extractor(x0)
#         # features_0_flatten = features_0.view(features_0.size(0), -1)
#         # # print(f'forward: features_0_flatten shape: {features_0_flatten.shape}')
#         #
#         # x1 = x[:, :, 1, :, :]
#         # features_1 = self.feature_extractor(x1)
#         # features_1_flatten = features_1.view(features_1.size(0), -1)
#         #
#         # x2 = x[:, :, 2, :, :]
#         # features_2 = self.feature_extractor(x2)
#         # features_2_flatten = features_2.view(features_2.size(0), -1)
#         #
#         # features_flatten = torch.cat((features_0_flatten, features_1_flatten, features_2_flatten), 1)
#         # print(f'forward: features_flatten shape: {features_flatten.shape}')
#         #
#         # class_scores = self.mlp(features_flatten)
#         #
#         # return class_scores