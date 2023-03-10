defmodule Takso.Accounts.Booking do
  use Ecto.Schema
  import Ecto.Changeset

  schema "bookings" do
    field :pickup_address, :string
    field :dropoff_address, :string

    timestamps()
  end

  @doc false
  def changeset(booking, attrs) do
    booking
    |> cast(attrs, [:pickup_address, :dropoff_address])
    |> validate_required([:pickup_address, :dropoff_address])
    |> validate_address_fields_not_same(:dropoff_address)
  end

  def validate_address_fields_not_same(changeset, field, options \\ []) do
    validate_change(changeset, field, fn _, dropoff_address ->
      pickup_address = get_field(changeset, :pickup_address)
      case pickup_address != dropoff_address do
        true -> []
        false -> [{field, options[:message] || "Dropoff and Pickup Address cannot be the same"}]
      end
    end)
  end
end
