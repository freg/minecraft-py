from typing import List, Tuple

class Chunk:
    def __init__(self, x: int, z: int, blocks: List[List[List[int]]] = None):
        self.x = x
        self.z = z
        self.blocks = blocks or [[[0 for _ in range(16)] for _ in range(256)] for _ in range(16)]

    def __eq__(self, other):
        if not isinstance(other, Chunk):
            return False
        return self.x == other.x and self.z == other.z and self.blocks == other.blocks

    def __repr__(self):
        return f"Chunk(x={self.x}, z={self.z}, blocks={self.blocks})"