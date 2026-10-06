# CyberNova Analytics: Design Documentation

Design artefacts produced for the CyberNova Analytics website. For setup instructions, see the [main README](../README.md).

## Requirements Summary

### Visitors can

- View cybersecurity solutions, case studies, technical blog articles and a photo gallery
- Read approved customer testimonials with star ratings, and submit their own
- Submit the **Contact Security Team** form (name, email, phone, organisation, country, job title, issue type, description) and receive an on-screen confirmation

### The admin can

- Log in securely and log out
- View all inquiries and filter them by service type
- View analytics on most requested services and regional demand
- Approve or reject submitted testimonials
- Create, edit and publish blog posts
- Manage solutions, case studies and gallery images

### Non-functional

- Responsive on desktop and mobile
- Clear, consistent navigation and a professional appearance
- Admin panel restricted to authenticated users

### Constraints

- Prototype scope: a single admin account and no public registration
- Free and open-source tools only

### Wish list (future work)

- Export inquiries to CSV
- Email notification on new inquiries

## Use Case Diagram

Two actors, the Visitor and the Admin. Form validation is an `«include»` of both submission use cases, and filtering by service is an `«extend»` of viewing inquiries.

![Use case diagram](diagrams/use-case-diagram.png)

## Entity Relationship Diagram

Seven tables. `ADMIN` is the parent of every other table, and `TESTIMONIAL.admin_id` is nullable because visitors submit testimonials before an admin approves them.

![ERD](diagrams/erd.png)

| Table           | Purpose                                              |
| --------------- | ---------------------------------------------------- |
| `ADMIN`         | The single administrator account (hashed password)   |
| `INQUIRY`       | Contact form submissions and their status            |
| `TESTIMONIAL`   | Visitor testimonials, shown publicly once approved   |
| `BLOG_POST`     | Technical articles (draft / published / archived)    |
| `SOLUTION`      | Services on the solutions page, with a display order |
| `CASE_STUDY`    | Past threat-mitigation projects                      |
| `GALLERY_IMAGE` | Uploaded gallery photos with captions and categories |

## System Flowcharts

| Contact form submission                                            | Admin login                                |
| ------------------------------------------------------------------ | ------------------------------------------ |
| ![Contact form submission](flowcharts/contact-form-submission.png) | ![Admin login](flowcharts/admin-login.png) |

| Inquiry management                                       | Testimonial approval                                         |
| -------------------------------------------------------- | ------------------------------------------------------------ |
| ![Inquiry management](flowcharts/inquiry-management.png) | ![Testimonial approval](flowcharts/testimonial-approval.png) |

## Wireframes

### Public pages

| Home                         | Case studies                                 |
| ---------------------------- | -------------------------------------------- |
| ![Home](wireframes/home.png) | ![Case studies](wireframes/case-studies.png) |

| Blog                         | Gallery                            |
| ---------------------------- | ---------------------------------- |
| ![Blog](wireframes/blog.png) | ![Gallery](wireframes/gallery.png) |

**Contact form**

![Contact form](wireframes/contact.png)

### Admin

| Login                                      | Dashboard                                  |
| ------------------------------------------ | ------------------------------------------ |
| ![Admin login](wireframes/admin-login.png) | ![Admin panel](wireframes/admin-panel.png) |
