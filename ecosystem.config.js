module.exports = {
  apps: [
    {
      name: "rasa-backend",
      script: "./scripts/start-rasa-backend.sh",
      interpreter: "bash",
      cwd: "/home/s_winklerf23/apps/mika-backend",
    },
    {
      name: "rasa-actions",
      script: "./scripts/start-rasa-actions.sh",
      interpreter: "bash",
      cwd: "/home/s_winklerf23/apps/mika-backend",
    },
  ],
};
