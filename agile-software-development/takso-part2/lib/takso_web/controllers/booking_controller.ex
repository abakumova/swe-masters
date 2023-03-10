defmodule TaksoWeb.BookingController do
  use TaksoWeb, :controller

  import Ecto.Query

  alias Takso.Repo
  alias Takso.Accounts.Booking
  alias Takso.{Repo, Accounts.Booking, Sales.Taxi}

  def new(conn, _params) do
    changeset = Booking.changeset(%Booking{}, %{})
    render(conn, "new.html", changeset: changeset)
  end

  def create(conn, %{"booking" => booking}) do
    changeset = Booking.changeset(%Booking{}, booking)

    case Repo.insert(changeset) do
      {:ok, _booking} ->
        query = from t in Taxi, where: t.status == "available", select: t
        available_taxis = Repo.all(query)

        case length(available_taxis) > 0 do
          true -> conn
                  |> put_flash(:info, "Your taxi will arrive in 7 minutes")
                  |> redirect(to: Routes.booking_path(conn, :new))
          _    -> conn
                  |> put_flash(:info, "At present, there is no taxi available!")
                  |> redirect(to: Routes.booking_path(conn, :new))
        end
      {:error, changeset} ->
        render(conn, "new.html", changeset: changeset)
    end
  end

end
