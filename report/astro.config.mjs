import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import mdx from "@astrojs/mdx";

export default defineConfig({
  site: "https://tabramovskaya.github.io/sml-multi-channel-communication",
  base: "/REPO",

  vite: {
    plugins: [tailwindcss()],
  },

  integrations: [mdx()],

  markdown: {
    shikiConfig: {
      theme: "css-variables",
    },
  },
});