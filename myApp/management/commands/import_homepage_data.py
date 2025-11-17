"""
Management command to import/seed homepage data into the database.
This command creates initial content for the iRiseUp Foundation website.
"""

from django.core.management.base import BaseCommand
from myApp.models import (
    SEO, Navigation, Hero, About, Stat, Program,
    FeaturedStory, Retreat, Testimonial, ImpactStory, CallToAction,
    Contact, ContactInfo, SocialLink, Footer, Event
)


class Command(BaseCommand):
    help = 'Import/seed initial homepage data into the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data import...'))
        
        # SEO
        self.stdout.write('Creating SEO data...')
        seo, created = SEO.objects.get_or_create(page='home', defaults={
            'title': 'iRiseUp Foundation - Helping Hearts Rise',
            'description': 'Empowering individuals and communities through leadership, mentorship, and education. Supporting programs in the US and Philippines.',
            'keywords': 'nonprofit, foundation, community, mentorship, education, Philippines, youth, leadership',
            'og_title': 'iRiseUp Foundation - Helping Hearts Rise',
            'og_description': 'Empowering individuals and communities through leadership, mentorship, and education.',
        })
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ SEO created'))
        else:
            self.stdout.write(self.style.WARNING('  - SEO already exists'))
        
        # Navigation
        self.stdout.write('Creating navigation...')
        nav_items = [
            {'label': 'Home', 'url': '/', 'sort_order': 1},
            {'label': 'About', 'url': '/about/', 'sort_order': 2},
            {'label': 'Core Beliefs', 'url': '/core-beliefs/', 'sort_order': 3},
            {'label': 'What We Do', 'url': '/what-we-do/', 'sort_order': 4},
            {'label': 'Events', 'url': '/events/', 'sort_order': 5},
            {'label': 'Mission Accomplished', 'url': '/mission-accomplished/', 'sort_order': 6},
            {'label': 'Contact', 'url': '/contact/', 'sort_order': 7},
        ]
        for item in nav_items:
            nav, created = Navigation.objects.get_or_create(
                label=item['label'],
                defaults={'url': item['url'], 'sort_order': item['sort_order']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Navigation item: {item["label"]}'))
        
        # Hero
        self.stdout.write('Creating hero section...')
        hero, created = Hero.objects.get_or_create(page='home', defaults={
            'label': 'NON-PROFIT FOUNDATION · GLOBAL COMMUNITY',
            'headline': 'Helping hearts rise, communities heal, and young lives thrive.',
            'subtext': 'Empowering individuals and communities through leadership, mentorship, and education. We support programs in the US and Philippines that help people thrive, not just survive.',
            'primary_button_text': 'Give a Love Gift',
            'primary_button_url': '/donate/',
            'secondary_button_text': 'Explore Our Mission',
            'secondary_button_url': '/about/',
        })
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ Hero created'))
        
        # About
        self.stdout.write('Creating about section...')
        about, created = About.objects.get_or_create(page='home', defaults={
            'label': 'ABOUT',
            'heading': 'We are ambassadors for belonging.',
            'description': 'iRiseUp Foundation is a non-profit community supporting programs focused on mentorship, education, and empowerment. We believe that everyone deserves to belong, to thrive, and to rise above their circumstances. From inner-city kids to coastal communities in the Philippines, we show up where hope is needed.',
        })
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ About created'))
        
        # Stats
        self.stdout.write('Creating statistics...')
        stats_data = [
            {'icon': 'fas fa-child', 'number': '500+', 'label': 'Children reached through Feed. Teach. Love.', 'sort_order': 1},
            {'icon': 'fas fa-campground', 'number': '200+', 'label': 'Youth empowered through camps', 'sort_order': 2},
            {'icon': 'fas fa-globe-americas', 'number': '15+', 'label': 'Communities served in Philippines & US', 'sort_order': 3},
            {'icon': 'fas fa-calendar-alt', 'number': '2021', 'label': 'Year of founding', 'sort_order': 4},
        ]
        for stat_data in stats_data:
            stat, created = Stat.objects.get_or_create(
                number=stat_data['number'],
                label=stat_data['label'],
                defaults={
                    'icon': stat_data['icon'],
                    'sort_order': stat_data['sort_order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Stat: {stat_data["number"]} - {stat_data["label"]}'))
        
        # Programs
        self.stdout.write('Creating programs...')
        programs_data = [
            {
                'label': 'PROGRAM',
                'title': 'Leadership Development',
                'description': 'Empowering individuals to become leaders in their communities through mentorship, training, and personal development programs.',
                'icon': 'fas fa-user-graduate',
                'learn_more_url': '/what-we-do/',
                'sort_order': 1
            },
            {
                'label': 'PROGRAM',
                'title': 'Feed. Teach. Love.',
                'description': 'Providing meals, education, and love to children in need. Nourishing bodies, minds, and hearts in communities across the Philippines and US.',
                'icon': 'fas fa-heart',
                'learn_more_url': '/what-we-do/',
                'sort_order': 2
            },
            {
                'label': 'PROGRAM',
                'title': 'Mental Health & Wellness',
                'description': 'Supporting mental health and emotional well-being through counseling, support groups, and wellness programs.',
                'icon': 'fas fa-brain',
                'learn_more_url': '/what-we-do/',
                'sort_order': 3
            },
            {
                'label': 'PROGRAM',
                'title': 'Youth Camps (Yes to Life!)',
                'description': 'Transformative camp experiences that inspire youth to say "Yes to Life!" Building confidence, community, and character.',
                'icon': 'fas fa-campground',
                'learn_more_url': '/what-we-do/',
                'sort_order': 4
            },
            {
                'label': 'PROGRAM',
                'title': 'Education & Training',
                'description': 'Providing educational opportunities and skills training to empower individuals and communities for long-term success.',
                'icon': 'fas fa-book',
                'learn_more_url': '/what-we-do/',
                'sort_order': 5
            },
            {
                'label': 'PROGRAM',
                'title': 'Disaster Relief',
                'description': 'Responding to natural disasters with immediate aid and long-term rebuilding efforts, especially in the Philippines.',
                'icon': 'fas fa-hammer',
                'learn_more_url': '/what-we-do/',
                'sort_order': 6
            },
        ]
        for prog_data in programs_data:
            program, created = Program.objects.get_or_create(
                title=prog_data['title'],
                defaults={
                    'label': prog_data['label'],
                    'description': prog_data['description'],
                    'icon': prog_data['icon'],
                    'learn_more_url': prog_data['learn_more_url'],
                    'sort_order': prog_data['sort_order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Program: {prog_data["title"]}'))
        
        # Featured Story
        self.stdout.write('Creating featured story...')
        story, created = FeaturedStory.objects.get_or_create(page='home', defaults={
            'label': 'FEATURED STORY',
            'quote': 'I want people to thrive, not just survive.',
            'quote_author': '',
            'title': 'Feed. Teach. Love.',
            'description': 'Feed. Teach. Love. is more than a program—it\'s a movement. We provide nutritious meals to children who need them most, but we don\'t stop there. We teach, we mentor, and most importantly, we show love. Every child deserves to know they matter.',
            'primary_button_text': 'Read the Story',
            'primary_button_url': '/mission-accomplished/',
            'secondary_button_text': 'Support Feed. Teach. Love.',
            'secondary_button_url': '/donate/',
        })
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ Featured story created'))
        
        # Retreat
        self.stdout.write('Creating retreat section...')
        retreat, created = Retreat.objects.get_or_create(page='home', defaults={
            'label': 'UPCOMING RETREAT',
            'title': 'A Heart of Remembrance',
            'date_range': 'May 23–26, 2025',
            'location': 'Mepkin Abbey Retreat Center · Moncks Corner, SC',
            'description': 'Join us for a time of spiritual reflection, remembrance, and healing. A sacred space to honor the past, embrace the present, and look forward with hope.',
            'primary_button_text': 'View Retreat Details',
            'primary_button_url': '/events/',
            'secondary_button_text': 'Join the Interest List',
            'secondary_button_url': '/contact/',
            'is_active': True
        })
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ Retreat created'))
        
        # Testimonials
        self.stdout.write('Creating testimonials...')
        testimonials_data = [
            {
                'name': 'Marvy S.',
                'role': 'Participant',
                'quote': 'iRiseUp changed my life. The mentorship I received helped me see my own potential and gave me the courage to pursue my dreams.',
                'icon': 'fas fa-user',
                'sort_order': 1
            },
            {
                'name': 'Joshua',
                'role': 'Supporter',
                'quote': 'Seeing the impact in the Philippines firsthand was incredible. These programs are truly transforming communities.',
                'icon': 'fas fa-user',
                'sort_order': 2
            },
            {
                'name': 'Emily D.',
                'role': 'Donor',
                'quote': 'I love knowing my donation is going directly to programs that make a real difference. The transparency and impact are clear.',
                'icon': 'fas fa-user',
                'sort_order': 3
            },
        ]
        for test_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                name=test_data['name'],
                role=test_data['role'],
                defaults={
                    'quote': test_data['quote'],
                    'icon': test_data['icon'],
                    'sort_order': test_data['sort_order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Testimonial: {test_data["name"]}'))
        
        # Impact Stories
        self.stdout.write('Creating impact stories...')
        impact_stories_data = [
            {
                'title': 'CLICK',
                'subtitle': 'Computer Learning for Inner City Kids',
                'description': 'Providing technology access and education to underserved youth, opening doors to new possibilities. Through CLICK, children who had never touched a computer are now learning coding, digital skills, and discovering their potential.',
                'icon': 'fas fa-laptop',
                'impact_points': ['100+ children reached', 'Technology labs established', 'Scholarships awarded'],
                'support_url': '/donate/',
                'sort_order': 1
            },
            {
                'title': 'Rebuilding Philippines',
                'subtitle': 'Disaster Response & Recovery',
                'description': 'Responding to natural disasters with immediate aid and long-term rebuilding efforts. After Storm Paeng/Nalgae, we provided emergency supplies, rebuilt homes, and restored hope to affected communities.',
                'icon': 'fas fa-hammer',
                'impact_points': ['50+ families supported', 'Homes rebuilt', 'Communities restored'],
                'support_url': '/donate/',
                'sort_order': 2
            },
            {
                'title': 'Yes to Life! Youth Camp',
                'subtitle': 'Transformative Camp Experience',
                'description': 'Transformative camp experiences that inspire youth to embrace life fully. Building confidence, community, and character. Youth leave with new friendships, renewed hope, and the courage to say "Yes to Life!"',
                'icon': 'fas fa-fire',
                'impact_points': ['200+ youth empowered', 'Lifelong friendships formed', 'Confidence built'],
                'support_url': '/donate/',
                'sort_order': 3
            },
        ]
        for story_data in impact_stories_data:
            story, created = ImpactStory.objects.get_or_create(
                title=story_data['title'],
                defaults={
                    'subtitle': story_data['subtitle'],
                    'description': story_data['description'],
                    'icon': story_data['icon'],
                    'impact_points': story_data['impact_points'],
                    'support_url': story_data['support_url'],
                    'sort_order': story_data['sort_order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Impact story: {story_data["title"]}'))
        
        # Call to Action
        self.stdout.write('Creating call to action...')
        cta, created = CallToAction.objects.get_or_create(page='home', defaults={
            'heading': 'Rise with us.',
            'subtext': 'Whether you give, volunteer, or share our mission, your yes helps someone else rise.',
            'primary_button_text': 'Give a Love Gift',
            'primary_button_url': '/donate/',
            'background_color': 'navy'
        })
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ Call to action created'))
        
        # Contact Info
        self.stdout.write('Creating contact info...')
        contact_info_data = [
            {'label': 'Address', 'value': 'Columbus, OH', 'icon': 'fas fa-map-marker-alt', 'sort_order': 1},
            {'label': 'Email', 'value': 'info@iriseupfoundation.org', 'icon': 'fas fa-envelope', 'sort_order': 2},
            {'label': 'Phone', 'value': '(614) 555-0123', 'icon': 'fas fa-phone', 'sort_order': 3},
        ]
        for info_data in contact_info_data:
            info, created = ContactInfo.objects.get_or_create(
                label=info_data['label'],
                defaults={
                    'value': info_data['value'],
                    'icon': info_data['icon'],
                    'sort_order': info_data['sort_order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Contact info: {info_data["label"]}'))
        
        # Social Links
        self.stdout.write('Creating social links...')
        social_links_data = [
            {'platform': 'facebook', 'url': '#', 'icon': 'fab fa-facebook', 'sort_order': 1},
            {'platform': 'instagram', 'url': '#', 'icon': 'fab fa-instagram', 'sort_order': 2},
            {'platform': 'twitter', 'url': '#', 'icon': 'fab fa-twitter', 'sort_order': 3},
            {'platform': 'linkedin', 'url': '#', 'icon': 'fab fa-linkedin', 'sort_order': 4},
        ]
        for link_data in social_links_data:
            link, created = SocialLink.objects.get_or_create(
                platform=link_data['platform'],
                defaults={
                    'url': link_data['url'],
                    'icon': link_data['icon'],
                    'sort_order': link_data['sort_order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Social link: {link_data["platform"]}'))
        
        # Footer
        self.stdout.write('Creating footer...')
        footer, created = Footer.objects.get_or_create(page='home', defaults={
            'about_text': 'Empowering individuals and communities through leadership, mentorship, and education. We are ambassadors for belonging.',
            'copyright_text': '© 2021–2025 iRiseUp Foundation. All rights reserved.'
        })
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ Footer created'))
        
        # Contact Page
        self.stdout.write('Creating contact page...')
        contact, created = Contact.objects.get_or_create(page='contact', defaults={
            'heading': "Let's Work Together",
            'subtext': 'Whether you want to volunteer, partner with us, or just learn more, we\'d love to hear from you.',
            'address': 'Columbus, OH',
            'email': 'info@iriseupfoundation.org',
            'phone': '(614) 555-0123'
        })
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ Contact page created'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Data import completed successfully!'))
        self.stdout.write(self.style.SUCCESS('You can now access the dashboard at /dashboard/ and edit this content.'))

