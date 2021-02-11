<script>
    import {Router} from "@roxi/routify";
    import {routes} from "../.routify/routes";
</script>

<style global type="text/scss" lang="scss">
  @import "../assets/main";

  @keyframes loading {
    0% {
      color: white;
      background-color: #085b8e;
    }
    50% {
      color: white;
      background-color: #2D9BF0;
    }
    100% {
      color: white;
      background-color: #085b8e;
    }
  }

  body {
    padding: 0;
    margin: 0;
    font-family: FreeSans -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
  }

  .muted {
    color: #999999;
  }

  .success {
    background-color: #79c21b;
    color: white;
  }


  .pending {
    background-color: white;
    color: black;
    animation: loading 2s linear infinite;
  }

  .failed {
    background-color: #F24726;
    color: white;
  }

  .info {
    background-color: #2D9BF0;
    color: white;
  }
</style>

<Router config="{{useHash: true}}" {routes}/>