---
name: Academic Residency System
colors:
  surface: '#fbf9f8'
  surface-dim: '#dcd9d9'
  surface-bright: '#fbf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f3f3'
  surface-container: '#f0eded'
  surface-container-high: '#eae8e7'
  surface-container-highest: '#e4e2e1'
  on-surface: '#1b1c1c'
  on-surface-variant: '#504441'
  inverse-surface: '#303030'
  inverse-on-surface: '#f2f0f0'
  outline: '#827470'
  outline-variant: '#d4c3be'
  surface-tint: '#77574d'
  primary: '#442a22'
  on-primary: '#ffffff'
  primary-container: '#5d4037'
  on-primary-container: '#d4ada1'
  inverse-primary: '#e7bdb1'
  secondary: '#75584d'
  on-secondary: '#ffffff'
  secondary-container: '#fed7ca'
  on-secondary-container: '#795c51'
  tertiary: '#402e00'
  on-tertiary: '#ffffff'
  tertiary-container: '#5d4300'
  on-tertiary-container: '#d9b058'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdbd0'
  primary-fixed-dim: '#e7bdb1'
  on-primary-fixed: '#2c160e'
  on-primary-fixed-variant: '#5d4037'
  secondary-fixed: '#ffdbce'
  secondary-fixed-dim: '#e4beb2'
  on-secondary-fixed: '#2b160f'
  on-secondary-fixed-variant: '#5b4137'
  tertiary-fixed: '#ffdea1'
  tertiary-fixed-dim: '#ecc067'
  on-tertiary-fixed: '#261900'
  on-tertiary-fixed-variant: '#5c4200'
  background: '#fbf9f8'
  on-background: '#1b1c1c'
  surface-variant: '#e4e2e1'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 16px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 32px
  xl: 48px
  container-max: 1280px
  gutter: 24px
---

## Brand & Style
The design system is engineered for a high-trust government portal managing student housing. The brand personality is **Authoritative, Grounded, and Accessible**. It balances the tradition of institutional oversight with the modern needs of a digital-first student population.

The design style follows a **Modern Corporate** aesthetic with **Tactile** accents. It leverages "warm professionalism" by using earthy tones to move away from cold, sterile government interfaces, instead evoking the physical environment of a well-maintained campus. The UI uses generous whitespace to reduce cognitive load during complex administrative tasks like registration and room selection.

## Colors
The palette is built on a foundation of "Heritage Browns" to convey stability.
- **Primary (#5D4037):** Used for navigation, primary buttons, and authoritative headers.
- **Secondary (#8D6E63):** Used for secondary actions and decorative UI elements.
- **Accent (#AF8936):** A bronze/gold used sparingly for highlight states, active indicators, and official seals to denote institutional excellence.
- **Functional:** Standard semantic colors are tuned for high accessibility (WCAG AA+) against the cream background.
- **Background (#FAFAFA):** A warm off-white that reduces eye strain compared to pure white, paired with soft grey (#F5F5F5) for section nesting.

## Typography
The design system utilizes **Inter** for its exceptional legibility in data-heavy forms and functional dashboards. 
- **Headlines:** Use a bold weight with slight negative letter-spacing to appear more authoritative and compact.
- **Body Text:** Set with generous line-height to ensure readability of housing policies and terms of service.
- **Labels:** Use semi-bold or medium weights to ensure they are distinct from input text, aiding users with visual impairments.

## Layout & Spacing
The design system employs a **Fixed Grid** strategy for desktop (12 columns) to maintain a centered, professional "portal" feel, transitioning to a **Fluid Grid** for tablet and mobile.

- **Desktop (1200px+):** 12 columns, 24px gutters, 48px margins.
- **Tablet (768px - 1199px):** 8 columns, 16px gutters, 24px margins.
- **Mobile (<767px):** 4 columns, 16px gutters, 16px margins.

Vertical rhythm is strictly maintained using multiples of 8px (base spacing unit). Dashboard cards should use `lg` (32px) padding to create an airy, premium feel.

## Elevation & Depth
Depth is created through **Tonal Layering** and **Soft Ambient Shadows**. 
- **Level 0 (Background):** #FAFAFA.
- **Level 1 (Cards/Containers):** Pure white (#FFFFFF) with a very soft, diffused shadow: `0px 4px 20px rgba(93, 64, 55, 0.08)`. The slight brown tint in the shadow ensures it feels integrated with the brand color.
- **Level 2 (Modals/Dropdowns):** White with a more pronounced shadow: `0px 8px 30px rgba(93, 64, 55, 0.12)`.
- **Interactions:** Hover states on cards should slightly lift (increase shadow) or use a 2px interior border in the Bronze accent color.

## Shapes
In line with the "Modern Professional" style, the design system uses a **Rounded** (0.5rem / 8px) base corner radius for standard elements like buttons and inputs. Larger containers like **Dashboard Cards** and **Modals** utilize `rounded-lg` (1rem / 16px) to soften the institutional feel and make the portal more welcoming to students.

## Components
- **Buttons:** Primary buttons are Solid Primary (#5D4037) with white text. Secondary buttons use an Outline style with a 1.5px stroke. 
- **Form Fields:** Use a light grey background (#F5F5F5) for the input area with a 1px bottom border that transitions to the Bronze accent on focus. Labels are always persistent above the field.
- **Status Badges:** Use low-saturation background tints of the functional colors with high-saturation text for maximum legibility (e.g., Success: Light green background, Dark green text).
- **Steppers:** For multi-step registration, use a horizontal bar with Bronze connectors and numbered circles. Completed steps are marked with a Primary Brown checkmark.
- **Upload Areas:** Large dashed-border zones with a secondary background tint. Use a "Cloud Upload" icon in Primary Brown as the focal point.
- **Data Tables:** Clean, no vertical borders. Use a Primary Brown header row with white text to ground the information.