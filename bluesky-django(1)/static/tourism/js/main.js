document.addEventListener("DOMContentLoaded", () => {
  // Smooth scrolling for navigation links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute("href"))
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })

  // Add scroll effect to header
  window.addEventListener("scroll", () => {
    const header = document.querySelector(".header")
    if (window.scrollY > 100) {
      header.style.background = "linear-gradient(135deg, rgba(30,60,114,0.95), rgba(42,82,152,0.95))"
      header.style.backdropFilter = "blur(10px)"
    } else {
      header.style.background = "linear-gradient(135deg, #1e3c72, #2a5298)"
      header.style.backdropFilter = "none"
    }
  })

  // Animate cards on scroll
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1"
        entry.target.style.transform = "translateY(0)"
      }
    })
  }, observerOptions)

  // Observe all cards
  const cards = document.querySelectorAll(".destination-card, .club-card, .offer-card, .testimonial")
  cards.forEach((card) => {
    card.style.opacity = "0"
    card.style.transform = "translateY(30px)"
    card.style.transition = "opacity 0.6s ease, transform 0.6s ease"
    observer.observe(card)
  })

  // Set minimum date to today for date picker
  const departInput = document.getElementById("depart")
  if (departInput) {
    const today = new Date().toISOString().split("T")[0]
    departInput.setAttribute("min", today)
  }

  // Price animation on hover
  document.querySelectorAll(".price").forEach((price) => {
    price.addEventListener("mouseenter", function () {
      this.style.transform = "scale(1.1)"
      this.style.transition = "transform 0.3s ease"
    })

    price.addEventListener("mouseleave", function () {
      this.style.transform = "scale(1)"
    })
  })

  // Close alert messages
  document.querySelectorAll(".close-alert").forEach((button) => {
    button.addEventListener("click", function () {
      this.parentElement.style.display = "none"
    })
  })

  // Auto-hide messages after 5 seconds
  setTimeout(() => {
    document.querySelectorAll(".alert").forEach((alert) => {
      alert.style.opacity = "0"
      alert.style.transform = "translateX(100%)"
      setTimeout(() => alert.remove(), 300)
    })
  }, 5000)

  // Mobile menu toggle (for future implementation)
  function toggleMobileMenu() {
    const navMenu = document.querySelector(".nav-menu")
    navMenu.classList.toggle("active")
  }

  // Add mobile menu button if needed
  if (window.innerWidth <= 768) {
    const navContainer = document.querySelector(".nav-container")
    const mobileMenuBtn = document.createElement("button")
    mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>'
    mobileMenuBtn.className = "mobile-menu-btn"
    mobileMenuBtn.onclick = toggleMobileMenu
    navContainer.appendChild(mobileMenuBtn)
  }

  // Gestion du formulaire de réservation - Version corrigée
  console.log("Recherche des éléments du formulaire de réservation...")

  const showFormBtn = document.getElementById("showReservationForm")
  const hideFormBtn = document.getElementById("hideReservationForm")
  const reservationForm = document.getElementById("reservationForm")

  console.log("showFormBtn:", showFormBtn)
  console.log("hideFormBtn:", hideFormBtn)
  console.log("reservationForm:", reservationForm)

  if (showFormBtn) {
    showFormBtn.addEventListener("click", (e) => {
      e.preventDefault()
      console.log("Bouton cliqué!")

      if (reservationForm) {
        reservationForm.style.display = "block"
        showFormBtn.style.display = "none"
        // Scroll vers le formulaire
        reservationForm.scrollIntoView({ behavior: "smooth", block: "nearest" })
      }
    })
  } else {
    console.log("Bouton showReservationForm non trouvé!")
  }

  if (hideFormBtn) {
    hideFormBtn.addEventListener("click", (e) => {
      e.preventDefault()
      console.log("Bouton annuler cliqué!")

      if (reservationForm) {
        reservationForm.style.display = "none"
        if (showFormBtn) {
          showFormBtn.style.display = "block"
        }
      }
    })
  }

  // Calculer le prix total en temps réel
  const travelersSelect = document.querySelector('select[name="travelers_count"]')
  const priceDisplay = document.querySelector(".price")

  if (travelersSelect && priceDisplay) {
    // Récupérer le prix de base depuis l'élément HTML
    const priceElement = priceDisplay.querySelector('div[style*="font-size: 2.5rem"]')
    if (priceElement) {
      const basePriceText = priceElement.textContent.replace("€", "").trim()
      const basePrice = Number.parseFloat(basePriceText) || 0

      travelersSelect.addEventListener("change", function () {
        const travelers = Number.parseInt(this.value) || 1
        const totalPrice = basePrice * travelers

        // Mettre à jour l'affichage du prix
        priceElement.innerHTML = totalPrice + '€ <small style="font-size: 0.6em;">total</small>'
      })
    }
  }

  // Définir la date minimum à aujourd'hui pour le formulaire de réservation
  const departureDateInput = document.querySelector('input[name="departure_date"]')
  if (departureDateInput) {
    const today = new Date().toISOString().split("T")[0]
    departureDateInput.setAttribute("min", today)
  }
})

// Function to format currency
function formatCurrency(amount) {
  return new Intl.NumberFormat("fr-FR", {
    style: "currency",
    currency: "EUR",
  }).format(amount)
}

// Function to calculate discount percentage
function calculateDiscount(original, current) {
  if (original > current) {
    return Math.round(((original - current) / original) * 100)
  }
  return 0
}

// Version alternative si les IDs ne fonctionnent pas
document.addEventListener("click", (e) => {
  // Gestion du bouton "Réserver maintenant"
  if (
    e.target.textContent.includes("Réserver maintenant") ||
    e.target.closest("button")?.textContent.includes("Réserver maintenant")
  ) {
    e.preventDefault()
    console.log("Bouton réserver détecté via event delegation!")

    const form = document.querySelector('div[id="reservationForm"], div[style*="display: none"]')
    const btn = e.target.closest("button")

    if (form && btn) {
      form.style.display = "block"
      btn.style.display = "none"
      form.scrollIntoView({ behavior: "smooth", block: "nearest" })
    }
  }

  // Gestion du bouton "Annuler"
  if (e.target.textContent.includes("Annuler") || e.target.closest("button")?.textContent.includes("Annuler")) {
    e.preventDefault()
    console.log("Bouton annuler détecté!")

    const form = e.target.closest("div").querySelector("form").parentElement
    const showBtn = document.querySelector('button[style*="display: none"]')

    if (form) {
      form.style.display = "none"
    }
    if (showBtn) {
      showBtn.style.display = "block"
    }
  }
})
