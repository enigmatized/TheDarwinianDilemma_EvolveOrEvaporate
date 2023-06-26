import akka.actor.ActorSystem
import akka.http.scaladsl.Http
import akka.http.scaladsl.model.HttpMethods._
import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.server.Route
import akka.stream.ActorMaterializer

import scala.io.StdIn

object HelloWorld {
  def main(args: Array[String]): Unit = {
    implicit val system = ActorSystem("hello-world-system")
    implicit val materializer = ActorMaterializer()
    implicit val executionContext = system.dispatcher

    val routes: Route = path("hello") {
      get {
        complete("Hello, World!")
      }
    }

    val bindingFuture = Http().bindAndHandle(routes, "localhost", 8080)

    println(s"Server online at http://localhost:8080/\nPress RETURN to stop...")
    StdIn.readLine()

    bindingFuture
      .flatMap(_.unbind())
      .onComplete(_ => system.terminate())
  }
}
