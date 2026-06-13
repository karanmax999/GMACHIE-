/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        space: {
          950: "#07090E",
          900: "#0B0F19",
          800: "#161D30",
          700: "#222D47",
        },
        accent: {
          indigo: "#6366F1",
          cyan: "#06B6D4",
          violet: "#8B5CF6",
          emerald: "#10B981",
        }
      },
      animation: {
        'pulse-glow': 'pulseGlow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 0.5s ease-out forwards',
        'slide-up': 'slideUp 0.4s ease-out forwards',
      },
      keyframes: {
        pulseGlow: {
          '0%, 100%': { 
            borderColor: 'rgba(99, 102, 241, 0.2)',
            boxShadow: '0 0 5px rgba(99, 102, 241, 0.05)'
          },
          '50%': { 
            borderColor: 'rgba(6, 182, 212, 0.6)',
            boxShadow: '0 0 20px rgba(6, 182, 212, 0.2)'
          },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        }
      }
    },
  },
  plugins: [],
}
