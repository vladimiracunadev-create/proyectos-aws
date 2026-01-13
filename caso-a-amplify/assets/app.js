(() => {
  const now = new Date();
  const $ = (id) => document.getElementById(id);

  $("now").textContent = now.toLocaleString();
  $("path").textContent = location.pathname;

  $("btn").addEventListener("click", () => {
    $("msg").textContent = "JS OK ✅ — " + new Date().toLocaleTimeString();
  });
})();
