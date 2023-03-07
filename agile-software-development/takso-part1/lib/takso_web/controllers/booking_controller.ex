defmodule TaksoWeb.BookingController do
  use TaksoWeb, :controller

  alias Takso.Repo
  alias Takso.Accounts.Booking

  def index(conn, _params) do
    render(conn, "index.html")
  end

  def booking(conn, _params) do
    render(conn, "booking.html")
  end

  def new(conn, _params) do
    render conn, "new.html"
  end

  def create(conn, %{"booking" => booking}) do
    changeset = Booking.changeset(%Booking{}, booking)

    case Repo.insert(changeset) do
      {:ok, booking} ->
        conn
        |> put_flash(:info, "Your taxi will arrive in 7 minutes")
        |> redirect(to: Routes.booking_path(conn, :index))
      {:error, changeset} ->
        render(conn, "new.html", changeset: changeset)
    end
  end

end
