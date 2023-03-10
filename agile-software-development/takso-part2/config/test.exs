import Config

# Configure your database
#
# The MIX_TEST_PARTITION environment variable can be used
# to provide built-in test partitioning in CI environment.
# Run `mix help test` for more information.
config :takso, Takso.Repo,
  username: "postgres",
  password: "test",
  hostname: "localhost",
  database: "takso_test#{System.get_env("MIX_TEST_PARTITION")}",
  pool: Ecto.Adapters.SQL.Sandbox,
  pool_size: 10

# We don't run a server during test. If one is required,
# you can enable the server option below.
config :takso, TaksoWeb.Endpoint,
  http: [ip: {127, 0, 0, 1}, port: 4001],
  secret_key_base: "Eu1F0jPsf53tMZCMGDdb4wRUo5vVRyrp7xDLt37BLF+vvkxYTRl7ZztXI48fOzAy",
  server: true

# In test we don't send emails.
config :takso, Takso.Mailer, adapter: Swoosh.Adapters.Test

# Print only warnings and errors during test
config :logger, level: :warn

# Initialize plugs at runtime for faster test compilation
config :phoenix, :plug_init_mode, :runtime
config :hound, driver: "chrome_driver"
config :takso, sql_sandbox: true
config :hound_playground, HoundPlayground.Endpoint,
  http:  [ip: {127, 0, 0, 1}, port: 4001],
  server: true
