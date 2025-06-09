module.exports = {
  apps: [
    {
      name: "mika-backend",
      script: "./scripts/start-rasa-backend.sh",
      interpreter: "bash",
      cwd: "/home/s_winklerf23/apps/mika-backend",
    },
    // {
    //   name: "mika-actions",
    //   script: "./scripts/start-rasa-actions.sh",
    //   interpreter: "bash",
    //   cwd: "/home/s_winklerf23/apps/mika-backend",
    // },
  ],
};
