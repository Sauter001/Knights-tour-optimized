drs, dcs = [-2, -2, -1, -1, 1, 1, 2, 2], [-1, 1, -2, 2, -2, 2, -1, 1]
directions = list(zip(drs, dcs))

"""
해당 위치 (r, c)로 이동 가능한지 확인하는 함수

@param r: row index
@param c: column index  
@param n: 체스판의 크기 (n x n)
@return: 이동 가능하면 True, 그렇지 않으면 False
"""
def is_movable(r, c, n):
    return 0 <= r < n and 0 <= c < n

def degree(r, c, board, n):
    cnt = 0
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if is_movable(nr, nc, n) and not board[nr][nc]:
            cnt += 1
    return cnt

def tour(path_r: list, path_c: list, start: tuple, board: list, n: int):
    # 모든 칸을 순회하면 결과 반환
    if len(path_r) == n * n and len(path_c) == n * n:
        return path_r, path_c
    stack = []
    stack.append(start)
    
    while stack:
        node = stack.pop()
        # 현재 위치 방문 처리
        board[node[0]][node[1]] = True
        
        candidates = []
        for dr, dc in directions:
            r, c = node
            nr, nc = r + dr, c + dc
            if is_movable(nr, nc, n):
                candidates.append((nr, nc))
                
        # 후보 중 다음에 이동 가능한 칸이 가장 작은 것 추출 (Warnsdorff's rule)
        # 방문한 칸까지 고려하여 후보를 필터링한다. 최소 칸인 경우 빼고 나머지는 배제
        candidates = [c for c in candidates if not board[c[0]][c[1]]]
        if candidates:
            # 후보들의 방문 가능칸 수 모으기
            moves_count = []
            for candidate in candidates:
                count = degree(candidate[0], candidate[1], board, n)
                moves_count.append((count, candidate))
            
            min_move_count = min(moves_count, key=lambda x: x[0])[0]
            # 후보 중 최소 이동 가능 칸을 가진 후보들만 추출
            candidates = [c for c in moves_count if c[0] == min_move_count]
            
            if len(candidates) == 1:
                next_move = candidates[0][1]
            else:
                # 후보가 여러 개일 경우, 그 다음 칸의 최소 차수가 가장 작은 것을 선택
                next_candidates = []
                for candidate in candidates:
                    count, (cr, cc) = candidate
                    board[cr][cc] = True  # 현재 후보 칸 방문 처리
                    min_next_degree = 9 # 최대 8방향이므로 9로 초기화. 다음 이동 가능 칸이 없을 경우 배제됨
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if is_movable(nr, nc, n) and not board[nr][nc]:
                            next_degree = degree(nr, nc, board, n)
                            if next_degree < min_next_degree:
                                min_next_degree = next_degree
                    next_candidates.append((min_next_degree, (cr, cc)))
                    board[cr][cc] = False  # 후보 칸 방문 처리 해제
                    
                next_move = min(next_candidates, key=lambda x: x[0])[1]
            
            board[next_move[0]][next_move[1]] = True
            path_r.append(next_move[0])
            path_c.append(next_move[1])
            stack.append(next_move)
            node = next_move  
        if not candidates:
            break
            
    return path_r, path_c

def main():
    n = int(input())
    r, c = tuple(map(int, input().split()))
    r, c = r - 1, c - 1  # 입력은 1-indexed이므로 0-indexed로 변환
    board = [[False] * n for _ in range(n)]
    path_r, path_c = tour([r], [c], (r, c), board, n)

    if len(path_r) == n * n:
        for i in range(n * n):
            print(path_r[i] + 1, path_c[i] + 1)
    else:
        print(-1, -1)

if __name__ == '__main__':
    main()