library(shiny)
library(shinyjs)
# library()

ui <- fluidPage(
  useShinyjs(),
  dataTableOutput("myTable"),
)

server <- function(input, output, session) {
  # 生成一个数据表
  output$myTable <- renderDataTable({
    data <- data.frame(
      Name = c("John", "Alice", "Bob"),
      Age = c(30, 25, 35)
    )
    datatable(data)
  })

  # 使用onFlushed来在数据表刷新后执行JavaScript代码
  observeEvent(input$myTable_rows_all, {
    js$onFlushed("myTable", code = "alert('数据表已刷新')")
  })
}

shinyApp(ui, server)
