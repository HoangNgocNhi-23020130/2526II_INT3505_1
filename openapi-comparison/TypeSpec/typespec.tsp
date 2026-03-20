import "@typespec/http";
import "@typespec/openapi";
using TypeSpec.Http;
using TypeSpec.OpenAPI;

@service(#{
  title: "Library Management API"
})

@doc("API đơn giản để quản lý đầu sách trong thư viện.")
@server("http://127.0.0.1:4010", "Mock Server")
namespace LibraryApi;

model Book {
  @extension("x-example", 1) id: int32;
  @extension("x-example", "De men phieu luu ky") title: string;
  @extension("x-example", "To Hoai") author: string;
  @extension("x-example", "978-6042168673") isbn: string;
}

model ArrayResponse {
  @extension("x-example", true) success: boolean;
  @extension("x-example", "Success!") message: string;
  data: {
    items: Book[];
  };
}

model ObjectResponse {
  @extension("x-example", true) success: boolean;
  @extension("x-example", "Success!") message: string;
  data: Book;
}

@error
model NotFoundResponse {
  @statusCode _: 404;
  @extension("x-example", false) success: boolean;
  @extension("x-example", "Not Found the book!") message: string;
  @extension("x-example", null) data: unknown;
}

@route("/books")
@tag("Books")
interface BooksOperations {
  @get
  @summary("Get all books")
  @doc("Return a list of books")
  @operationId("getBooks")
  
  list(): ArrayResponse;

  @route("{id}")
  @get
  @summary("Get detail a book")
  @operationId("getBook")
  read(@path id: int32): ObjectResponse | NotFoundResponse;
}