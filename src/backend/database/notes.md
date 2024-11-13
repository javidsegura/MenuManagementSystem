Link to the ER diagram: [click here](https://lucid.app/lucidchart/8efdf10f-0814-413c-9af0-3ed3754c3ff3/edit?invitationId=inv_02075271-b8c7-4567-9cbc-a5f36854fafc&page=0_0#)


# dataDefinition.sql 
Schame Notes:
1) A user can publish 0 or many posts
2) Each posts contains a menu. It may be a new version of the same manu or a new menu
3) Each menu version has its one and only one menu content
4) Each menu content has 1 or many sections
5) Each section has 1 or many items
6) Several items may have several allergies 
7) Each menu_version belongs to a restaurant
8) Many restaurants have many opening_hours (possible overlapping)
9) Each menu_version has one and only logger audit

Thing to do:
0) Reimplement manually (written for me: Javi; feel free to ignore)
1) Add more defaults if applicable


