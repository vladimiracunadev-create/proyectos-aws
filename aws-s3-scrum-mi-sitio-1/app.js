(() => {
  // Año footer
  const y = document.getElementById("y");
  if (y) y.textContent = String(new Date().getFullYear());

  // Reveal on scroll (con fallback)
  const els = Array.from(document.querySelectorAll(".reveal"));

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
    els.forEach((el) => el.classList.add("show"));
  }

  // === Modo rápido (compacto) ===
  const modeBtn = document.getElementById("modeBtn");
  const saved = localStorage.getItem("viewMode"); // "compact" | "full"

  const setModeUI = (isCompact) => {
    if (!modeBtn) return;
    modeBtn.setAttribute("aria-pressed", isCompact ? "true" : "false");
    modeBtn.textContent = isCompact ? "✅ Modo rápido" : "⚡ Modo rápido";
    modeBtn.title = isCompact ? "Mostrar todo el contenido" : "Oculta detalles largos";
  };

  if (saved === "compact") {
    document.body.classList.add("compact");
    setModeUI(true);
  } else {
    setModeUI(false);
  }

  if (modeBtn) {
    modeBtn.addEventListener("click", () => {
      const isCompact = document.body.classList.toggle("compact");
      localStorage.setItem("viewMode", isCompact ? "compact" : "full");
      setModeUI(isCompact);
    });
  }
})();
