/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        wood: "#4CAF50",
        fire: "#F44336",
        earth: "#FF9800",
        metal: "#FFC107",
        water: "#2196F3",
      },
    },
  },
  plugins: [],
};
