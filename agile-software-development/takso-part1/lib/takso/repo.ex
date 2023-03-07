defmodule Takso.Repo do
  use Ecto.Repo,
    otp_app: :takso,
    adapter: Ecto.Adapters.Postgres
end
