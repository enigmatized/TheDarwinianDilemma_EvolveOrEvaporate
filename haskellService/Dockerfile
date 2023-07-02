FROM haskell:latest

WORKDIR /app

COPY . .



# Docker will cache this command as a layer, freeing us up to
# modify source code without re-installing dependencies
# (unless the .cabal file changes!)
RUN stack build


# Add and Install Application Code

CMD ["stack run"]
