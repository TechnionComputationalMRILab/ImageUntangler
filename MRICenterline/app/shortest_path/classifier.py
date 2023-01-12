import torch
from abc import ABC, abstractmethod
from torch import Tensor, nn


class Classifier(nn.Module, ABC):
    def __init__(self, model: nn.Module):
        super().__init__()
        self.model = model

    def forward(self, x: Tensor) -> [Tensor, Tensor]:
        z: Tensor = None
        # print(f'{x.size()=}')
        z = self.model(x)
        return z
    
    def predict_proba(self, x: Tensor) -> Tensor:
        z = self.model(x)
        return self.predict_proba_scores(z)

    def predict_proba_scores(self, z: Tensor) -> Tensor:
        m = nn.Softmax(dim=1)
        # m = nn.Sigmoid()
        prob = m(z)
        return prob

    def predict_proba_scores_numpy(self, z):
        m = nn.Softmax(dim=1)
        # m = nn.Sigmoid()
        prob = m(torch.from_numpy(z))
        return prob.numpy()

    def classify(self, x: Tensor) -> Tensor:
        y_proba = self.predict_proba(x)
        return self._classify(y_proba)

    def classify_scores(self, z: Tensor) -> Tensor:
        y_proba = self.predict_proba_scores(z)
        return self._classify(y_proba)

    @abstractmethod
    def _classify(self, y_proba: Tensor) -> Tensor:
        pass


class ArgMaxClassifier(Classifier):
    def _classify(self, y_proba: Tensor):
        _, max_indices = torch.topk(y_proba, k=2, dim=1)
        max_indices = max_indices.sort(dim=1).values
        # _, max_indices = torch.max(y_proba, dim=1)
        return max_indices