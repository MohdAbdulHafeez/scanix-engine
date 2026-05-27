"use client"

import Navbar from "@/components/scan/Navbar"
import Hero from "@/components/scan/Hero"
import WhyScanix from "@/components/scan/WhyScanix"
import InsightSection from "@/components/scan/InsightSection"
import HealthGoals from "@/components/scan/HealthGoals"
import Testimonials from "@/components/scan/Testimonials"
import CTAFloat from "@/components/scan/CTAFloat"
import SectionWrapper from "@/components/scan/SectionWrapper"

export default function HomePage() {
  return (
    <main className="overflow-hidden">
      <Navbar />

      <SectionWrapper id="hero">
        <Hero />
      </SectionWrapper>

      <SectionWrapper id="why">
        <WhyScanix />
      </SectionWrapper>

      <SectionWrapper id="insights">
        <InsightSection />
      </SectionWrapper>

      <SectionWrapper id="goals">
        <HealthGoals />
      </SectionWrapper>

      <SectionWrapper id="testimonials">
        <Testimonials />
      </SectionWrapper>

      <SectionWrapper id="footer">
        <footer className="bg-[#F7F6F2] py-12 mt-20">
          <div className="max-w-[1280px] mx-auto px-10 flex justify-between items-center">
            <div className="text-[#247A51] font-black text-[24px]">SCANIX AI</div>
            <div className="text-[#667085] text-sm">
              © {new Date().getFullYear()} Scanix AI. All rights reserved.
            </div>
          </div>
        </footer>
      </SectionWrapper>

      {/* Floating CTA */}
      <CTAFloat />
    </main>
  )
}