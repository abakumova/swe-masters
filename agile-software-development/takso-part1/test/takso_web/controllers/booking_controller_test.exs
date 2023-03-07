defmodule TaksoWeb.BookingControllerTest do
  use TaksoWeb.ConnCase

  test "POST /bookings", %{conn: conn} do
    conn = post conn, "/bookings", %{booking: [pickup_address: "Liivi 2", dropoff_address: "Muuseumi tee 2"]}
    conn = get conn, redirected_to(conn)
    assert html_response(conn, 200) =~ ~r/Your taxi will arrive in \d+ minutes/
  end
end
