#encoding:utf-8
urls = (
'/admin/?',         'controller.admin.index',
'/admin/login',     'controller.admin.login',
'/admin/logout',    'controller.admin.logout',

#--------------user -----------
#----用户表，包含普通读者和图书管理员，超级管理员----
"/admin/user_list",            "controller.admin.user.user_list",
"/admin/user_read/(\d+)",      "controller.admin.user.user_read",
"/admin/user_edit/(\d+)",      "controller.admin.user.user_edit",
"/admin/user_delete/(\d+)",    "controller.admin.user.user_delete",
#--------------end user -------

#--------------book -----------
#----书籍信息----
"/admin/book_list",            "controller.admin.book.book_list",
"/admin/book_read/(\d+)",      "controller.admin.book.book_read",
"/admin/book_edit/(\d+)",      "controller.admin.book.book_edit",
"/admin/book_delete/(\d+)",    "controller.admin.book.book_delete",
#--------------end book -------

#--------------publisher -----------
#----出版商----
"/admin/public_list",            "controller.admin.publisher.publisher_list",
"/admin/public_read/(\d+)",      "controller.admin.publisher.publisher_read",
"/admin/public_edit/(\d+)",      "controller.admin.publisher.publisher_edit",
"/admin/public_delete/(\d+)",    "controller.admin.publisher.publisher_delete",
#--------------end publisher -------

#--------------author -----------
#----作者----
"/admin/author_list",            "controller.admin.author.author_list",
"/admin/author_read/(\d+)",      "controller.admin.author.author_read",
"/admin/author_edit/(\d+)",      "controller.admin.author.author_edit",
"/admin/author_delete/(\d+)",    "controller.admin.author.author_delete",
#--------------end author -------



)
