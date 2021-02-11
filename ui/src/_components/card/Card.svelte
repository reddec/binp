<script></script>
<style type="text/scss">
  @import "../../../assets/main";

  .card {
    display: flex;
    flex-direction: column;
    border-radius: $radius;
    border: 0.02rem solid black;
    padding: 0;
    margin: 0;
    background-color: white;
    overflow: hidden;
  }


</style>
<div class="card">
    <slot/>
</div>
