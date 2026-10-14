document.addEventListener("DOMContentLoaded", () => {
    const listeMenu = document.getElementById("liste-menu");
    const boutonsFiltre = document.querySelectorAll(".filtre");

    if (listeMenu) {
        let platsData = [];
        fetch("/api/menu")
            .then(res => res.json())
            .then(data => {
                platsData = data;
                afficherPlats(platsData);
            })
            .catch(err => console.error("Erreur API menu:", err));

        function afficherPlats(plats) {
            listeMenu.innerHTML = "";
            plats.forEach(p => {
                const li = document.createElement("li");
                li.style.padding = "0.5rem 0";
                li.style.borderBottom = "1px solid #eee";
                li.textContent = `${p.nom} — ${p.prix} XAF (${p.categorie})`;
                listeMenu.appendChild(li);
            });
        }

        boutonsFiltre.forEach(btn => {
            btn.addEventListener("click", () => {
                const cat = btn.getAttribute("data-categorie");
                if (cat === "tout") {
                    afficherPlats(platsData);
                } else {
                    afficherPlats(platsData.filter(p => p.categorie === cat));
                }
            });
        });
    }
});