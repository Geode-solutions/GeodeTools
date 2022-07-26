<!--
Copyright (c) 2019 - 2022 Geode-solutions

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-->

<template>
  <div>
    <v-tooltip bottom>
      <slot name="tooltip"></slot>
      <template #activator="{ on }">
        <v-btn
          icon
          absolute
          :style="btnStyle"
          v-on="on"
          @click="toggleValue = !toggleValue"
        >
          <slot name="btn" :btn-style="btnStyle"></slot>
        </v-btn>
      </template>
    </v-tooltip>
    <div ref="option" style="position: absolute">
      <slot v-if="toggleValue" name="option"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "ContextualItem",
  props: {
    left: {
      required: true,
      type: Number
    },
    top: {
      required: true,
      type: Number
    },
    btnSize: {
      required: true,
      type: Number
    },
    toggle: {
      type: Boolean,
      default: false
    },
    toggleInit: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    toggleValue: false
  }),
  computed: {
    btnStyle() {
      let style = {
        left: this.left + "px",
        top: this.top + "px",
        width: this.btnSize + "px",
        height: this.btnSize + "px"
      };
      if (this.toggle) {
        style.border = "1px solid " + this.color;
        if (this.toggleValue) {
          style.backgroundColor = this.color;
        }
      }
      return style;
    },
    color() {
      return getComputedStyle(document.documentElement).getPropertyValue(
        "--v-secondary-base"
      );
    }
  },
  watch: {
    toggleValue: function(value) {
      if (this.toggle) {
        this.$parent.$emit("toggle-change", value);
      }
    }
  },
  updated() {
    this.$nextTick(() => {
      const option = this.$refs.option;
      if (this.left < 0) {
        option.style.left = this.left - this.$refs.option.clientWidth + "px";
      } else {
        option.style.left = this.left + this.btnSize + "px";
      }
      if (this.top < 0) {
        option.style.top = this.top - this.$refs.option.clientHeight + "px";
      } else {
        option.style.top = this.top + this.btnSize + "px";
      }
    });
  },
  mounted() {
    this.$nextTick(() => {
      this.toggleValue = this.toggleInit;
    });
  }
};
</script>
