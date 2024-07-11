# Arbor Feeds

This will create a link to a Live Feed between this report and Excel, Google Sheets or a BI application. This means that the data in your spreadsheet or BI application will automatically update when it is updated in Arbor. We recommend using the HTML v2 option if you are using Arbor's Google Sheets connector.
Please be aware - if you share a document with a live feed to someone, they will have access to that data as long as they have access to the document.
For Live Feeds containing a large amount of data we recommend using an output format of JSON.

Click [here](http://bit.ly/using-live-feeds) for detailed instructions on how to connect to your Live Feed.

## KS3 Course/Class Memberships

URL: [https://fort-pitt-grammar-school.uk.arbor.sc/data-export/export/id/3/h/c5255bebc2e0a920/format/json/v/2/]
Authorization: Basic a2NhcnRlcjphNzE3M2U0MGE3ZTEzYWY4NTg2YzhkYjg2N2Q5Njg1ZjU0Yzk2NTQ3

= Json.Document(Web.Contents("https://fort-pitt-grammar-school.uk.arbor.sc/data-export/export/id/3/h/c5255bebc2e0a920/format/json/v/2/", [Headers=[Authorization="Basic a2NhcnRlcjphNzE3M2U0MGE3ZTEzYWY4NTg2YzhkYjg2N2Q5Njg1ZjU0Yzk2NTQ3"]]))

## Teaching Group Memberships: 2023/2024

URL: [https://fort-pitt-grammar-school.uk.arbor.sc/data-export/export/id/4/h/8adf8ad5d8ad643d/format/json/v/2/](https://fort-pitt-grammar-school.uk.arbor.sc/data-export/export/id/4/h/8adf8ad5d8ad643d/format/json/v/2/)
Authorization: Basic a2NhcnRlcjpiNGIwYmFmMWRiNDBkOGM0MDcyYTMxNjkwODQ5ZmM2OGY5YWZkODkx

= Web.Page(Web.Contents("https://fort-pitt-grammar-school.uk.arbor.sc/data-export/export/id/4/h/8adf8ad5d8ad643d/format/json/v/2/", [Headers=[Authorization="Basic a2NhcnRlcjpiNGIwYmFmMWRiNDBkOGM0MDcyYTMxNjkwODQ5ZmM2OGY5YWZkODkx"]])){0}[Data]

## Scheduled Timetable Slots

URL: [https://fort-pitt-grammar-school.uk.arbor.sc/data-export/export/id/6/h/d884125414d90c23/format/json/v/2/]
Authorization: Basic a2NhcnRlcjowNmM3ODA4YjE5NzI3M2ZmMGUxMGM1N2MzNTE0MDkzMzA4Yzk2NTY0

= Web.Page(Web.Contents("https://fort-pitt-grammar-school.uk.arbor.sc/data-export/export/id/6/h/d884125414d90c23/format/json/v/2/", [Headers=[Authorization="Basic a2NhcnRlcjowNmM3ODA4YjE5NzI3M2ZmMGUxMGM1N2MzNTE0MDkzMzA4Yzk2NTY0"]])){0}[Data]

## Behavioural Incidents Reporting

URL: [https://fort-pitt-grammar-school.uk.arbor.sc/data-export/export/id/7/h/73f7d5c93871aaf1/format/json/v/2/]
Authorization: Basic a2NhcnRlcjo0NzdmZGM0M2ExZGM5ZTljYzM3OTJiMzJhMzg5YTY1N2ZmMWJjM2Mx

= Web.Page(Web.Contents("https://fort-pitt-grammar-school.uk.arbor.sc/data-export/export/id/7/h/73f7d5c93871aaf1/format/json/v/2/", [Headers=[Authorization="Basic a2NhcnRlcjo0NzdmZGM0M2ExZGM5ZTljYzM3OTJiMzJhMzg5YTY1N2ZmMWJjM2Mx"]])){0}[Data]

## Y7 Lesson Timetable

URL: [https://fort-pitt-grammar-school.uk.arbor.sc/data-export/export/id/8/h/751a5387bf918c55/format/json/v/2/]
Authorization: Basic a2NhcnRlcjoyMjNhMGQ5YmI5ZWU3MDkwMDlkMjk5MTk2ZTY5MDI3NjllMGJiNDNj

= Json.Document(Web.Contents("https://fort-pitt-grammar-school.uk.arbor.sc/data-export/export/id/8/h/751a5387bf918c55/format/json/v/2/", [Headers=[Authorization="Basic a2NhcnRlcjoyMjNhMGQ5YmI5ZWU3MDkwMDlkMjk5MTk2ZTY5MDI3NjllMGJiNDNj"]]))