(() => {
  // Año footer
  const y = document.getElementById("y");
  if (y) y.textContent = String(new Date().getFullYear());

  // Reveal on scroll (con fallback)
  const els = Array.from(document.querySelectorAll(".reveal"));
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) if (e.isIntersecting) e.target.classList.add("show");
    }, { threshold: 0.12 });
    els.forEach(el => io.observe(el));
  } else {
    els.forEach(el => el.classList.add("show"));
  }

  // ===== Menú móvil =====
  const menuBtn = document.getElementById("menuBtn");
  const navMenu = document.getElementById("navMenu");
  const overlay = document.getElementById("overlay");

  const isMobile = () => window.matchMedia("(max-width: 980px)").matches;

  const openMenu = () => {
    if (!navMenu || !overlay || !menuBtn) return;
    navMenu.classList.add("open");
    overlay.hidden = false;
    menuBtn.setAttribute("aria-expanded", "true");
  };

  const closeMenu = () => {
    if (!navMenu || !overlay || !menuBtn) return;
    navMenu.classList.remove("open");
    overlay.hidden = true;
    menuBtn.setAttribute("aria-expanded", "false");
  };

  if (menuBtn) {
    menuBtn.addEventListener("click", () => {
      const open = navMenu.classList.contains("open");
      if (open) closeMenu(); else openMenu();
    });
  }

  if (overlay) overlay.addEventListener("click", closeMenu);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeMenu();
  });

  if (navMenu) {
    navMenu.addEventListener("click", (e) => {
      const t = e.target;
      if (!isMobile()) return;
      if (t && t.tagName === "A") closeMenu();
    });
  }

  // ===== Toast =====
  const toast = document.getElementById("toast");
  let toastTimer = null;

  const showToast = (msg) => {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("show"), 1400);
  };

  // ===== Animación show/hide para bloques Optional/Deep =====
  const prefersReduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const animateHide = (el) => {
    if (!el || el.dataset._hidden === "1") return;
    el.dataset._display = el.dataset._display || getComputedStyle(el).display || "block";

    if (prefersReduced) {
      el.style.display = "none";
      el.dataset._hidden = "1";
      return;
    }

    const start = el.getBoundingClientRect().height || el.scrollHeight || 0;
    el.style.overflow = "hidden";
    el.style.height = `${start}px`;
    el.style.opacity = "1";
    el.style.pointerEvents = "none";

    const anim = el.animate(
      [{ height: `${start}px`, opacity: 1 }, { height: "0px", opacity: 0 }],
      { duration: 220, easing: "ease-out", fill: "forwards" }
    );

    anim.onfinish = () => {
      el.style.display = "none";
      el.style.height = "";
      el.style.opacity = "";
      el.style.overflow = "";
      el.style.pointerEvents = "";
      el.dataset._hidden = "1";
    };
  };

  const animateShow = (el) => {
    if (!el) return;

    // Si ya está visible, no animar
    const computed = getComputedStyle(el).display;
    const isHidden = el.dataset._hidden === "1" || computed === "none";
    if (!isHidden) return;

    const display = el.dataset._display || "block";

    if (prefersReduced) {
      el.style.display = display;
      el.dataset._hidden = "0";
      return;
    }

    el.style.display = display;
    const end = el.scrollHeight || 0;

    el.style.overflow = "hidden";
    el.style.height = "0px";
    el.style.opacity = "0";
    el.style.pointerEvents = "none";

    const anim = el.animate(
      [{ height: "0px", opacity: 0 }, { height: `${end}px`, opacity: 1 }],
      { duration: 260, easing: "ease-out", fill: "forwards" }
    );

    anim.onfinish = () => {
      el.style.height = "";
      el.style.opacity = "";
      el.style.overflow = "";
      el.style.pointerEvents = "";
      el.dataset._hidden = "0";
    };
  };

  // ===== 3 VISTAS =====
  const viewChip = document.getElementById("viewChip");
  const viewSwitch = document.getElementById("viewSwitch");
  const viewBtns = viewSwitch ? Array.from(viewSwitch.querySelectorAll("[data-view]")) : [];
  const optionalEls = Array.from(document.querySelectorAll(".optional"));
  const deepEls = Array.from(document.querySelectorAll(".deep"));
  const accordions = Array.from(document.querySelectorAll("details.accordion"));

  const LABEL = {
    quick: "👔 Vista: Reclutador",
    normal: "👀 Vista: Normal",
    deep: "🧠 Vista: Profundo"
  };

  const setActiveBtn = (view) => {
    viewBtns.forEach(btn => btn.classList.toggle("active", btn.dataset.view === view));
  };

  const setChip = (view) => {
    if (!viewChip) return;
    viewChip.textContent = LABEL[view] || "Vista: Normal";
  };

  const setView = (view, announce = true) => {
    const v = (view === "quick" || view === "deep") ? view : "normal";

    // Estado en body (por si luego quieres estilos específicos)
    document.body.classList.toggle("view-quick", v === "quick");
    document.body.classList.toggle("view-deep", v === "deep");

    // Optional
    if (v === "quick") optionalEls.forEach(animateHide);
    else optionalEls.forEach(animateShow);

    // Deep-only
    if (v === "deep") deepEls.forEach(animateShow);
    else deepEls.forEach(animateHide);

    // Acordeones: en Profundo se abren, en otros se cierran
    if (v === "deep") accordions.forEach(d => d.open = true);
    else accordions.forEach(d => d.open = false);

    // UI
    setActiveBtn(v);
    setChip(v);

    localStorage.setItem("portfolioView", v);

    if (announce) {
      showToast(v === "quick" ? "👔 Vista Reclutador activada" :
                v === "deep" ? "🧠 Vista Profundo activada" :
                               "👀 Vista Normal activada");
    }
  };

  // Eventos botones
  viewBtns.forEach(btn => {
    btn.addEventListener("click", () => setView(btn.dataset.view));
  });

  // Restaurar preferencia
  const saved = localStorage.getItem("portfolioView") || "normal";
  setView(saved, false);
})();
