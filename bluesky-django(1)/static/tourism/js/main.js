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
