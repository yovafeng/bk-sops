/**
* Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
* Edition) available.
* Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
* Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
* http://opensource.org/licenses/MIT
* Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
* an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
* specific language governing permissions and limitations under the License.
*/
<template>
    <div class="palette-panel">
        <div class="palette-container">
            <div
                :class="[
                    'palette-item',
                    'entry-item',
                    { disabled: isDisableStartPoint }
                ]"
                data-config-name=""
                data-type="startpoint">
                <div :class="`node-type-icon common-icon-node-startpoint-${langSuffix}`"></div>
            </div>
            <div
                :class="[
                    'palette-item',
                    'entry-item',
                    { disabled: isDisableEndPoint }
                ]"
                data-config-name=""
                data-type="endpoint">
                <div :class="`node-type-icon common-icon-node-endpoint-${langSuffix}`"></div>
            </div>
            <div
                :class="['palette-item', 'entry-item', 'palette-with-menu', { actived: activeNodeListType === 'tasknode' }]"
                data-type="tasknode"
                @mousedown="onNodeMouseDown('tasknode', $event)">
                <div class="node-type-icon common-icon-node-tasknode"></div>
            </div>
            <div
                :class="['palette-item','entry-item', 'palette-with-menu', { actived: activeNodeListType === 'subflow' }]"
                data-type="subflow"
                @mousedown="onNodeMouseDown('subflow', $event)">
                <div class="node-type-icon common-icon-node-subflow"></div>
            </div>
            <div class="palette-item entry-item" data-config-name="" data-type="parallelgateway">
                <div class="node-type-icon common-icon-node-parallelgateway"></div>
            </div>
            <div class="palette-item entry-item" data-config-name="" data-type="branchgateway">
                <div class="node-type-icon common-icon-node-branchgateway"></div>
            </div>
            <div class="palette-item entry-item" data-config-name="" data-type="convergegateway">
                <div class="node-type-icon common-icon-node-convergegateway"></div>
            </div>
            <!-- <div class="palette-item entry-item" data-config-name="" data-type="conditionalparallelgateway">
                <div class="node-type-icon common-icon-node-conditionalparallelgateway"></div>
            </div> -->
        </div>
        <node-menu
            ref="node_menu"
            :show-node-menu="showNodeMenu"
            :is-fixed-node-menu="isFixedNodeMenu"
            :active-node-list-type="activeNodeListType"
            :template-labels="templateLabels"
            :loading="activeNodeListType === 'subflow' && listLoading"
            :nodes="nodes"
            :common="common"
            @onCloseNodeMenu="onCloseNodeMenu"
            @onToggleNodeMenuFixed="onToggleNodeMenuFixed">
        </node-menu>
    </div>
</template>
<script>
    import i18n from '@/config/i18n/index.js'
    import NodeMenu from './NodeMenu.vue'
    import Guide from '@/utils/guide.js'
    import { mapState, mapActions } from 'vuex'
    import permission from '@/mixins/permission.js'
    export default {
        name: 'PalattePanel',
        components: {
            NodeMenu
        },
        mixins: [permission],
        props: {
            templateLabels: Array,
            atomTypeList: {
                type: Object,
                default () {
                    return {}
                }
            },
            isDisableStartPoint: {
                type: Boolean,
                default: false
            },
            isDisableEndPoint: {
                type: Boolean,
                default: false
            },
            common: {
                type: [String, Number],
                default: false
            }
        },
        data () {
            return {
                activeNodeListType: '',
                showNodeMenu: false,
                isFixedNodeMenu: false,
                isMenuTypeChange: false,
                nodeMouse: {
                    type: '',
                    startX: null,
                    startY: null
                },
                moveFlag: {
                    x: 0,
                    y: 0
                },
                listLoading: true, // 列表加载loading
                currentPage: 0,
                limit: Math.ceil(((window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight) - 200) / 40) + 5,
                pollingTimer: null,
                isPageOver: false,
                isThrottled: false // 滚动节流 是否进入cd
            }
        },
        computed: {
            ...mapState({
                lang: state => state.lang
            }),
            langSuffix () {
                return this.lang === 'en' ? 'en' : 'zh'
            },
            nodes () {
                if (!this.activeNodeListType) {
                    return []
                }
                if (this.activeNodeListType === 'tasknode') {
                    return this.atomTypeList.tasknode
                } else {
                    return this.atomTypeList.subflow
                }
            }
        },
        watch: {
            showNodeMenu (val) {
                this.$emit('updateNodeMenuState', val)
            },
            activeNodeListType (val) {
                if (val === 'subflow') {
                    this.getSubflowList()
                    this.$nextTick(() => {
                        this.listNode = document.querySelector('.node-list-wrap')
                        this.listNode.addEventListener('scroll', this.handleTableScroll)
                    })
                } else {
                    this.currentPage = 0
                    this.atomTypeList.subflow.length = 0
                }
            }
        },
        mounted () {
            this.$emit('registerPaletteEvent')
            this.renderGuide()
        },
        methods: {
            ...mapActions('templateList', [
                'loadTemplateList'
            ]),
            async getSubflowList () {
                this.listLoading = true
                try {
                    const data = {
                        template_id: this.template_id,
                        limit: this.limit,
                        offset: this.currentPage * this.limit
                    }
                    const resp = await this.loadTemplateList(data)
                    this.handleSubflowList(resp)
                } catch (e) {
                    console.log(e)
                } finally {
                    this.listLoading = false
                }
            },
            handleTableScroll () {
                if (!this.isPageOver && !this.isThrottled) {
                    this.isThrottled = true
                    this.pollingTimer = setTimeout(() => {
                        this.isThrottled = false
                        const el = this.listNode
                        if (el.scrollHeight - el.offsetHeight - el.scrollTop < 10) {
                            this.currentPage += 1
                            this.isPageOver = this.currentPage === this.totalPage
                            clearTimeout(this.pollingTimer)
                            this.getSubflowList()
                        }
                    }, 500)
                }
            },
            handleSubflowList (data) {
                const list = []
                const reqPermission = this.common ? ['common_flow_view'] : ['flow_view']
                data.objects.forEach(item => {
                    // 克隆模板可以引用被克隆的模板，模板不可以引用自己
                    if (this.type === 'clone' || item.id !== Number(this.template_id)) {
                        item.hasPermission = this.hasPermission(reqPermission, item.auth_actions)
                        list.push(item)
                    }
                })
                this.atomTypeList.subflow.push(...list)
            },
            onMouseDown (e) {
                this.moveFlag = {
                    x: e.pageX,
                    y: e.pageY
                }
            },
            onOpenNodeMenu () {
                this.showNodeMenu = true
                this.activeNodeListType = this.nodeMouse.type
            },
            onCloseNodeMenu () {
                this.showNodeMenu = false
                this.activeNodeListType = ''
            },
            onToggleNodeMenuFixed (val) {
                this.isFixedNodeMenu = val
            },
            /**
             * 节点点击，区分是 展开菜单 还是 拖拽
             * @param {String} type -node type
             * @param {Object} e -event
             */
            onNodeMouseDown (type, e) {
                this.nodeMouse.startX = e.pageX
                this.nodeMouse.startY = e.pageY
                this.isMenuTypeChange = this.nodeMouse.type !== type
                this.nodeMouse.type = type
                document.addEventListener('mouseup', this.mouseUpHandler)
            },
            mouseUpHandler (e) {
                const endX = e.pageX
                const endY = e.pageY
                const max = Math.max(endX - this.nodeMouse.startX, endY - this.nodeMouse.startY)
                // 移动距离小于 3 像素，认为是点击事件
                if (max < 3) {
                    this.showNodeMenu && !this.isMenuTypeChange ? this.onCloseNodeMenu() : this.onOpenNodeMenu()
                }
                document.removeEventListener('mouseup', this.mouseUpHandler)
            },
            renderGuide () {
                const nodesGuide = [
                    {
                        el: '.entry-item[data-type=tasknode]',
                        url: require('@/assets/images/left-tasknode-guide.gif'),
                        text: [
                            {
                                type: 'name',
                                val: i18n.t('标准插件节点：')
                            },
                            {
                                type: 'text',
                                val: i18n.t('已封装好的可用插件，可直接选中拖拽至画布中。')
                            }
                        ]
                    },
                    {
                        el: '.entry-item[data-type=subflow]',
                        url: require('@/assets/images/left-subflow-guide.gif'),
                        text: [
                            {
                                type: 'name',
                                val: i18n.t('子流程：')
                            },
                            {
                                type: 'text',
                                val: i18n.t('同一个项目下已新建的流程，作为子流程可以嵌套进至当前流程，并在执行任务时可以操作子流程的单个节点。')
                            }
                        ]
                    },
                    {
                        el: '.entry-item[data-type=parallelgateway]',
                        url: require('@/assets/images/left-parallelgateway-guide.gif'),
                        text: [
                            {
                                type: 'name',
                                val: i18n.t('并行网关：')
                            },
                            {
                                type: 'text',
                                val: i18n.t('有多个流出分支，并且多个流出分支都默认执行。')
                            }
                        ]
                    },
                    {
                        el: '.entry-item[data-type=branchgateway]',
                        url: require('@/assets/images/left-branchgateway-guide.gif'),
                        text: [
                            {
                                type: 'name',
                                val: i18n.t('分支网关：')
                            },
                            {
                                type: 'text',
                                val: i18n.t('执行符合条件的流出分支。多个条件符合时，将只会执行第一个符合条件的分支。')
                            }
                        ]
                    },
                    {
                        el: '.entry-item[data-type=convergegateway]',
                        url: require('@/assets/images/left-convergegateway-guide.gif'),
                        text: [
                            {
                                type: 'name',
                                val: i18n.t('汇聚网关：')
                            },
                            {
                                type: 'text',
                                val: i18n.t('当汇聚网关用于汇聚并行网关时，所有进入顺序流的分支都到达以后，流程才会通过汇聚网关。')
                            }
                        ]
                    },
                    {
                        el: '.entry-item[data-type=conditionalparallelgateway]',
                        url: require('@/assets/images/left-branchgateway-guide.gif'),
                        text: [
                            {
                                type: 'name',
                                val: i18n.t('条件并行网关：')
                            },
                            {
                                type: 'text',
                                val: i18n.t('执行时满足分支条件的都会执行。')
                            }
                        ]
                    }
                ]
                const baseConfig = {
                    el: '',
                    width: 330,
                    delay: 500,
                    arrow: false,
                    placement: 'right',
                    trigger: 'mouseenter',
                    img: {
                        height: 155,
                        url: ''
                    },
                    text: []
                }
                nodesGuide.forEach(m => {
                    baseConfig.img.url = m.url
                    baseConfig.text = m.text
                    const guide = new Guide(baseConfig)
                    guide.mount(document.querySelector(m.el))
                })
            }
        }
    }
</script>
<style lang="scss" scoped>
    .palette-panel {
        position: relative;
        width: 60px;
        height: 100%;
        z-index: 5;
    }
    .palette-container{
        position: relative;
        height: 100%;
        border-right: 1px solid #cacedb;
        background: #ffffff;
        z-index: 3;
        .palette-item {
            padding: 15px 0;
            text-align: center;
            cursor: move;
            user-select: none;
            &:hover {
                .node-type-icon{
                    color: #3a84ff;
                }
            }
            &.disabled {
                opacity: 0.3;
                pointer-events: none;
            }
        }
        .palette-with-menu {
            position: relative;
            cursor: pointer;
            &.actived,
            &:hover {
                .node-type-icon {
                    color: #3a84ff;
                }
            }
        }
        .node-type-icon {
            font-size: 28px;
            color: #546a9e;
            &.common-icon-node-tasknode,
            &.common-icon-node-subflow {
                font-size: 20px;
            }
        }
    }
</style>
