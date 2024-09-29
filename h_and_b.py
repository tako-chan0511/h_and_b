import random
import streamlit as st
from itertools import permutations

# 4桁のランダムな数字を生成する関数
# 0～9の異なる4つの数字をランダムに選び、文字列として返す
def generate_answer():
    digits = random.sample(range(0, 10), 4)  # 0-9の中から重複なしで4つ選ぶ
    return ''.join(map(str, digits))  # 数字リストを文字列に変換して返す

# ヒットとブローを計算する関数
# 入力された数値(guess)と正解(answer)を比較し、ヒットとブローをカウントして返す
def calculate_hit_blow(guess, answer):
    # ヒット: 数字と位置が一致する場合の数
    hit = sum([1 for i in range(4) if guess[i] == answer[i]])
    # ブロー: 数字は一致しているが、位置が異なる場合の数
    blow = sum([1 for i in range(4) if guess[i] != answer[i] and guess[i] in answer])
    return hit, blow

# 可能な4桁のすべての組み合わせを生成（重複なし）
# 0-9の数字から4つの異なる数字を使った全組み合わせを生成
def generate_all_combinations():
    return [''.join(p) for p in permutations('0123456789', 4)]  # 0123456789から4桁の組み合わせを生成

# Streamlit アプリのメイン部分
st.title("★ヒット＆ブロー ゲーム★")

# 初期状態の確認と設定
# st.session_stateはStreamlitのセッション間でデータを保持するために使用される
if 'answer' not in st.session_state:  # ゲームが初回ならば初期化
    st.session_state['answer'] = generate_answer()  # 正解の4桁の数を生成
    st.session_state['attempts'] = 0  # 試行回数
    st.session_state['history'] = []  # 推測履歴を格納
    st.session_state['candidates'] = generate_all_combinations()  # 可能性のある全組み合わせ
    st.session_state['game_over'] = False  # ゲーム終了状態の管理フラグ

st.write("4桁の数字を推測して、ヒット＆ブローの結果を確認しよう！")
st.write("ヒットは位置も数字も一致している場合、ブローは数字だけ一致している場合です。")

# プレイヤーの入力（ゲーム終了前のみ表示）
if not st.session_state['game_over']:
    guess = st.text_input("4桁の数字を入力してください:", max_chars=4)

# ゲームロジック
# 「チェック！」ボタンが押されたら、ユーザー入力を評価してヒット＆ブローを計算
if st.button("チェック！") and not st.session_state['game_over']:
    if len(guess) == 4 and guess.isdigit() and len(set(guess)) == 4:  # 入力が正しいか確認
        st.session_state['attempts'] += 1  # 試行回数を1増やす
        hit, blow = calculate_hit_blow(guess, st.session_state['answer'])  # ヒット＆ブローを計算
        
        # 推測履歴を更新
        st.session_state['history'].append((guess, hit, blow))

        # 残りの候補を絞り込む
        # 推測結果（ヒット＆ブロー）に基づいて、候補リストを絞り込む
        st.session_state['candidates'] = [
            candidate for candidate in st.session_state['candidates'] 
            if calculate_hit_blow(guess, candidate) == (hit, blow)
        ]
        
        # 結果を表示
        st.write(f"結果: {hit} ヒット, {blow} ブロー")
        
        # 正解ならゲーム終了を通知
        if hit == 4:
            st.success(f"おめでとう！ 正解です！ 答えは {st.session_state['answer']} でした。")
            st.session_state['game_over'] = True  # ゲーム終了フラグをTrueに設定
        else:
            st.write(f"試行回数: {st.session_state['attempts']}")
            st.write(f"残りの候補数: {len(st.session_state['candidates'])}")
    else:
        # 入力が正しくない場合はエラーメッセージを表示
        st.error("4桁の数字を正しく入力してください（重複なし）。")

# ゲーム終了後のリロードメッセージ
# 正解後に再ゲームを促すメッセージを表示
if st.session_state['game_over']:
    st.warning("ゲームが終了しました。再ゲームを行うにはページをリロードしてください。")

# 候補表示のボタンと表示ロジック
# ボタンを押すことで候補リストを表示/非表示にする
if st.button("候補を表示"):
    st.session_state['show_candidates'] = not st.session_state.get('show_candidates', False)

# 残りの候補リストを表示
if st.session_state.get('show_candidates', False):
    st.write("残りの候補:")
    st.write(st.session_state['candidates'])

# 履歴を表示
# 今までの推測とヒット＆ブローの結果を表示する
if st.session_state['history']:
    st.write("これまでの推測結果:")
    for i, (guess, hit, blow) in enumerate(st.session_state['history'], 1):
        st.write(f"{i}: {guess} -> {hit} ヒット, {blow} ブロー")
