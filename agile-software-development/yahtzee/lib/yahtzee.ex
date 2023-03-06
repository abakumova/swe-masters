defmodule Yahtzee do
  def score_upper(dice) do
    %{Ones: length(Enum.filter(dice, fn e -> e == 1 end)),
    Twos: length(Enum.filter(dice, fn e -> e == 2 end)),
    Threes: length(Enum.filter(dice, fn e -> e == 3 end)),
    Fours: length(Enum.filter(dice, fn e -> e == 4 end)),
    Fives: length(Enum.filter(dice, fn e -> e == 5 end)),
    Sixes: length(Enum.filter(dice, fn e -> e == 6 end))}
  end

  defp consecutive([]), do: []
  defp consecutive([_ | []]), do: consecutive([])
  defp consecutive(dice), do: consecutive(dice, 0)
  defp consecutive([head | [head2 | []]], _) when head2 - head == 1, do: [head] ++ [head2]
  defp consecutive([head | [_| []]], _), do: [head | consecutive([])]
  defp consecutive([head | [head2 | tail]], n) when head2 - head == 1, do: [head | consecutive([head2 | tail], n + 1)]
  defp consecutive([head | [head2 | _]], n) when head2 - head != 1 and n > 0, do: consecutive([])
  defp consecutive([_ | tail], n), do: consecutive(tail, n + 1)

  def score_lower(dice) do
    sum = Enum.sum(dice)
    face_frequencies = Enum.frequencies(dice) |> Map.values() |> Enum.sort()

    formatted_roll = dice |> Enum.sort() |> Enum.uniq()
    straight_roll = consecutive(formatted_roll)

    %{
      "Three of a kind":
        if face_frequencies |> Enum.member?(3) do sum else 0 end,
      "Four of a kind":
        if face_frequencies |> Enum.member?(4)
        or face_frequencies |> Enum.member?(5) do sum else 0 end,
      "Full house":
        if face_frequencies |> Enum.member?(3) and face_frequencies |> Enum.member?(2) do 25 else 0 end,
      "Small straight":
        if ((face_frequencies == [1, 1, 1, 1, 1] or face_frequencies == [1, 1, 1, 2]) and length(straight_roll) == 4) do 30 else 0 end,
      "Large straight":
        if length(straight_roll) == 5 do 40 else 0 end,
      "Yahtzee":
        if face_frequencies |> Enum.member?(5) do 50 else 0 end,
      "Chance":
        if Enum.sort(face_frequencies) == [1, 2, 2] or ((face_frequencies == [1, 1, 1, 1, 1] or face_frequencies == [1, 1, 1, 2]) and length(straight_roll) < 4) do sum else 0 end,
    }
  end

  def score([]), do: %{}
  def score(dice), do: Map.merge(score_upper(dice), score_lower(dice))
end
