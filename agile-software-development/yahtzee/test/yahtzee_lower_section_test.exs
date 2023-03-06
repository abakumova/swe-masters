defmodule YahtzeeLowerSectionTest do
  use ExUnit.Case

  def generate(dice_face, occurrences) do
    Enum.to_list(1..6)
    |> List.delete(dice_face)
    |> Enum.shuffle
    |> Enum.take(5 - occurrences)
    |> Enum.concat(List.duplicate(dice_face, occurrences))
    |> Enum.shuffle
  end

  test "Identify 'Three of a kind' with ones" do
    dices = generate(1, 3)
    sum = Enum.sum(dices)
    assert %{"Three of a kind": ^sum} = Yahtzee.score_lower(dices)
  end

  test "Identify 'Three of a kind' with all the others" do
    Enum.map(2..6, fn (dice_face) ->
      dices = generate(dice_face, 3)
      sum = Enum.sum(dices)
      assert %{"Three of a kind": ^sum} = Yahtzee.score_lower(dices)
    end)
  end

  test "Identify 'Four of a kind' with every face" do
    Enum.map(1..6, fn (dice_face) ->
      dices = generate(dice_face, 4)
      sum = Enum.sum(dices)
      assert %{"Four of a kind": ^sum} = Yahtzee.score_lower(dices)
    end)
  end

  test "Identify 'Full house' with every face" do
    Enum.map(1..6, fn _ ->
      [x,y] =
        Enum.shuffle(1..6)
        |> Enum.take(2)
      assert %{"Full house": 25} = Yahtzee.score_lower([x,x,x,y,y] |> Enum.shuffle)
    end)
  end

  test "Identify 'Small straight'" do
    Enum.map(1..6, fn _ ->
      x = Enum.shuffle([1, 2, 3, 4, Enum.random([1, 2, 3, 4, 6])])
      y = Enum.shuffle([2, 3, 4, 5, Enum.random([2, 3, 4, 5])])
      z = Enum.shuffle([3, 4, 5, 6, Enum.random([1, 3, 4, 5, 6])])

      seq = Enum.random([x, y, z]) |> Enum.shuffle()
      assert %{"Small straight": 30} = Yahtzee.score_lower(seq)
    end)
  end

  test "Identify 'Large straight'" do
    Enum.map(1..6, fn _ ->
      x = Enum.shuffle([1, 2, 3, 4, 5])
      y = Enum.shuffle([2, 3, 4, 5, 6])

      seq = Enum.random([x, y]) |> Enum.shuffle()
      assert %{"Large straight": 40} = Yahtzee.score_lower(seq)
    end)
  end

  test "Identify 'Yahtzee'" do
    Enum.map(1..6, fn n ->
      assert %{Yahtzee: 50} = Yahtzee.score_lower(List.duplicate(n,5))
    end)
  end

  test "Identify any other combination" do
    Enum.map(1..6, fn _ ->
      [x,y,z] =
        Enum.shuffle(1..6)
        |> Enum.take(3)
      seq = Enum.shuffle([x,x,y,y,z])
      sum = Enum.sum(seq)
      assert %{Chance: ^sum} = Yahtzee.score_lower(seq)
    end)
  end

  test "Identify dice configuration of 2 twos and 3 Fives" do
    seq = [2, 5, 2, 5, 5] |> Enum.shuffle
    sum = Enum.sum(seq)

    assert %{
      "Ones": 0,
      "Twos": 2,
      "Threes": 0,
      "Fours": 0,
      "Fives": 3,
      "Sixes": 0,
      "Three of a kind": ^sum,
      "Four of a kind": 0,
      "Full house": 25,
      "Small straight": 0,
      "Large straight": 0,
      "Chance": 0,
      "Yahtzee": 0
    } = Yahtzee.score(seq)
  end

  test "Identify a combination with no duplicates and no 'Straight's" do
    seq = [1, 2, 3, 5, 6] |> Enum.shuffle
    sum = Enum.sum(seq)

    assert %{
      "Ones": 1,
      "Twos": 1,
      "Threes": 1,
      "Fours": 0,
      "Fives": 1,
      "Sixes": 1,
      "Three of a kind": 0,
      "Four of a kind": 0,
      "Full house": 0,
      "Small straight": 0,
      "Large straight": 0,
      "Chance": ^sum,
      "Yahtzee": 0
    } = Yahtzee.score(seq)
  end

  test "Identify a combination with no 'Chance' and 'Small straight'" do
    seq = [1, 3, 4, 5, 6] |> Enum.shuffle

    assert %{
      "Ones": 1,
      "Twos": 0,
      "Threes": 1,
      "Fours": 1,
      "Fives": 1,
      "Sixes": 1,
      "Three of a kind": 0,
      "Four of a kind": 0,
      "Full house": 0,
      "Small straight": 30,
      "Large straight": 0,
      "Chance": 0,
      "Yahtzee": 0
    } = Yahtzee.score(seq)
  end

  test "Identify 'Yahtzee' also as 'Four of a kind'" do
    seq = [3, 3, 3, 3, 3]
    sum = Enum.sum(seq)

    assert %{
      "Ones": 0,
      "Twos": 0,
      "Threes": 5,
      "Fours": 0,
      "Fives": 0,
      "Sixes": 0,
      "Three of a kind": 0,
      "Four of a kind": ^sum,
      "Full house": 0,
      "Small straight": 0,
      "Large straight": 0,
      "Chance": 0,
      Yahtzee: 50
    } = Yahtzee.score(seq)
  end

end
