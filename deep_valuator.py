import torch
import torch.nn.functional as F
from reinforcement_learning.model import Model
from reinforcement_learning import generate_data

from state import Board


class DeepValuator:
    def __init__(self, weights_path, device="cpu"):
        self.device = device
        self.model = self.__load_model(weights_path)
    
    def __load_model(self, weights_path):
        model = Model().to(self.device)
        state_dict = torch.load(weights_path)
        model.load_state_dict(state_dict)
        model.eval()
        return model
    
    def __call__(self, board):
        board = generate_data.parse_move(board.__str__())
        board = board.reshape((1, -1))
        board = torch.from_numpy(board).float().to(self.device)
        score = self.model(board)
        score = torch.softmax(score, dim=1)[0]
        score = score[2] - score[0]
        return score.item()

    
if __name__ == '__main__':
    val = DeepValuator("/data.local/giangh/ml_course_project/reinforcement_learning/ckpt/0.5040.pth", "cuda:0")
    board = Board()
    print(val(board))