{-# LANGUAGE DataKinds #-}
{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE TypeOperators #-}

module Main (main) where

import Lib
import GHC.Generics
import Network.Wai.Handler.Warp (run)
import Servant

-- Define the API type
type HelloWorldAPI = "hello" :> Get '[PlainText] String

-- Implement the API handlers
helloHandler :: Handler String
helloHandler = return "Hello, World!"

-- Specify the API
helloWorldAPI :: Proxy HelloWorldAPI
helloWorldAPI = Proxy

-- Combine the API and handlers
app :: Application
app = serve helloWorldAPI helloHandler

-- Start the server
main :: IO ()
main = run 8085 app
