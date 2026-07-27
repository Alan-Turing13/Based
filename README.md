*Based* is a Full-stack Knowledge Repository & Query Engine I built using Django ORM.

![Add Author](static/examples/add-author.png)

I wanted to build a content management system serving theological and philosophical quotes.

![Welcome Page](static/examples/welcome-page.png)

First I designed a normalised SQLite schema with multi-table relationships (`ForeignKey` linking Quotes, Authors and Categorised Subjects). 

![Table](static/examples/table.png)

For the Security pipeline, I implemented custom session-based Auth with protected view-level permissions (`LoginRequiredMixin`), so that only registered & signed-in users could post quotes, and only the user that create a post could edit or delete it. For user registration I automated SMTP token validation so that a valid email address would be required to create an account.

![Sign in](static/examples/sign-in.png)

Entity attribution metadata such as `added_at` and `added_by` lends the service a social element. I have also implemented multi-attribute query filtering and paginated querysets to make the data more accessible. Users can search by quote text, author name, source and subject.

![Search](static/examples/search.png)