(() => {
  // Año footer
  const y = document.getElementById("y");
  if (y) y.textContent = String(new Date().getFullYear());

  // Reveal on scroll (con fallback)
  const els = Array.from(document.querySelectorAll(".reveal"));

  if (!els.length) return;

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) e.target.classList.add("show");
        }
      },
      { threshold: 0.12 }
    );

    els.forEach((el) => io.observe(el));
  } else {
    // Fallback: mostrar todo (navegadores viejos)
    els.forEach((el) => el.classList.add("show"));
  }
})();
