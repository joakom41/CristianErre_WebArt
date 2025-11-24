/**
 * Tailwind config for django-tailwind
 * Configuración personalizada para galería de arte minimalista
 */
module.exports = {
  content: [
    // Templates dentro de theme (si los hay)
    "../templates/**/*.html",

    // Templates globales en el proyecto
    "../../cristianerre_art/templates/**/*.html",
    "../../core/templates/**/*.html",
    "../../core/templates/core/**/*.html",
    "../../catalogo/templates/**/*.html",
    "../../catalogo/templates/catalogo/**/*.html",

    // Cualquier otro HTML del proyecto
    "../../**/*.html",
  ],
  theme: {
    extend: {
      // Paleta de colores personalizada para galería de arte
      colors: {
        'art-bg': '#fafaf9',      // stone-50
        'art-text': '#1c1917',    // stone-900
        'art-muted': '#57534e',   // stone-600
        'art-border': '#d6d3d1',  // stone-300
        'art-accent': '#292524',  // stone-800
      },
      
      // Tipografía elegante
      fontFamily: {
        'display': ['Playfair Display', 'serif'],
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
      
      // Animaciones personalizadas
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(30px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-1000px 0' },
          '100%': { backgroundPosition: '1000px 0' },
        },
      },
      animation: {
        'fade-in': 'fadeIn 0.6s ease-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'scale-in': 'scaleIn 0.4s ease-out',
        'shimmer': 'shimmer 2s infinite linear',
      },
      
      // Sombras sutiles y profesionales
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
        'soft-lg': '0 10px 40px -10px rgba(0, 0, 0, 0.1), 0 20px 25px -5px rgba(0, 0, 0, 0.04)',
        'soft-xl': '0 20px 50px -12px rgba(0, 0, 0, 0.15), 0 30px 40px -10px rgba(0, 0, 0, 0.08)',
      },
      
      // Transiciones suaves
      transitionDuration: {
        '400': '400ms',
        '600': '600ms',
      },
    },
  },
  plugins: [],
};
