# -*- coding:utf-8 -*-
import unittest
import mock

from ..models.soft_deletable import QuerySetProxy


class QuerySetProxyTestCase(unittest.TestCase):
    def test_init_should_set_query(self):
        # setup
        query = mock.Mock()
        proxy = QuerySetProxy(query)

        # assert
        self.assertEqual(id(query), id(proxy.wrapped_query))

    def test_wrap_should_return_query_attribute_value(self):
        # setup
        query = mock.Mock()
        query.configure_mock(attribute=True)
        proxy = QuerySetProxy(query)

        # action
        returned_value = proxy.wrap('attribute')

        # assert
        self.assertTrue(query.attribute)

    def test_wrap_return_method_return_value_called_with_arguments(self):
        # setup
        method = mock.Mock()

        class MockQuery(object):
            def method(self, *args, **kwargs):
                return method(*args, **kwargs)

        proxy = QuerySetProxy(MockQuery())
        args = (1, 2, 3,)
        kwargs = dict(one=1, two=2, three=3)

        # action
        returned_value = proxy.wrap('method')(*args, **kwargs)
        
        # assert
        self.assertTupleEqual((args, kwargs,), method.call_args)
        self.assertEqual(id(method.return_value), id(returned_value))

    def test_wrap_return_method_return_query_set_proxy_if_result_is_query_set(
            self):
        # setup
        method = mock.Mock()

        class MockQuery(object):
            def method(self, *args, **kwargs):
                return QuerySetProxy(method(*args, **kwargs))

        with mock.patch('libs.models.soft_deletable.QuerySet', MockQuery):
            proxy = QuerySetProxy(MockQuery())
            args = (1, 2, 3,)
            kwargs = dict(one=1, two=2, three=3)

            # action
            returned_value = proxy.wrap('method')(*args, **kwargs)
            
            # assert
            self.assertTupleEqual((args, kwargs,), method.call_args)
            self.assertEqual(id(method.return_value),
                id(returned_value.wrapped_query))

    def test_deepcopy_should_return_deepcopy_via_wrap(self):
        # setup
        proxy = QuerySetProxy(mock.Mock())
        wrap = mock.Mock()
        proxy.wrap = wrap

        # action
        returned_value = proxy.__deepcopy__({})

        # assert
        self.assertTupleEqual(('__deepcopy__',), wrap.call_args[0])
        self.assertTupleEqual(({},), wrap.return_value.call_args[0])
        self.assertEqual(id(wrap.return_value.return_value), id(returned_value))

    def test_getstate_should_return_getstate_via_wrap(self):
        # setup
        proxy = QuerySetProxy(mock.Mock())
        wrap = mock.Mock()
        proxy.wrap = wrap

        # action
        returned_value = proxy.__getstate__()

        # assert
        self.assertTupleEqual(('__getstate__',), wrap.call_args[0])
        self.assertEqual(id(wrap.return_value.return_value), id(returned_value))

    def test_repr_should_return_repr_via_wrap(self):
        # setup
        proxy = QuerySetProxy(mock.Mock())
        wrap = mock.Mock()
        proxy.wrap = wrap

        # action
        returned_value = proxy.__repr__()

        # assert
        self.assertTupleEqual(('__repr__',), wrap.call_args[0])
        self.assertEqual(id(wrap.return_value.return_value), id(returned_value))

    def test_len_should_return_len_via_wrap(self):
        # setup
        proxy = QuerySetProxy(mock.Mock())
        wrap = mock.Mock()
        proxy.wrap = wrap

        # action
        returned_value = proxy.__len__()

        # assert
        self.assertTupleEqual(('__len__',), wrap.call_args[0])
        self.assertEqual(id(wrap.return_value.return_value), id(returned_value))

    def test_iter_should_return_iter_via_wrap(self):
        # setup
        proxy = QuerySetProxy(mock.Mock())
        wrap = mock.Mock()
        proxy.wrap = wrap

        # action
        returned_value = proxy.__iter__()

        # assert
        self.assertTupleEqual(('__iter__',), wrap.call_args[0])
        self.assertEqual(id(wrap.return_value.return_value), id(returned_value))

    def test_nonzero_should_return_nonzerp_via_wrap(self):
        # setup
        proxy = QuerySetProxy(mock.Mock())
        wrap = mock.Mock()
        proxy.wrap = wrap

        # action
        returned_value = proxy.__nonzero__()

        # assert
        self.assertTupleEqual(('__nonzero__',), wrap.call_args[0])
        self.assertEqual(id(wrap.return_value.return_value), id(returned_value))

    def test_getitem_should_call_getitem_via_wrap(self):
        # setup
        proxy = QuerySetProxy(mock.Mock())
        wrap = mock.Mock()
        proxy.wrap = wrap
        key = 1

        # action
        returned_value = proxy.__getitem__(key)

        # assert
        self.assertTupleEqual(('__getitem__',), wrap.call_args[0])
        self.assertTupleEqual((key,), wrap.return_value.call_args[0])
        self.assertEqual(id(wrap.return_value.return_value), id(returned_value))

    def test_and_call_and_via_wrap(self):
        # setup
        proxy = QuerySetProxy(mock.Mock())
        wrap = mock.Mock()
        proxy.wrap = wrap
        other = mock.Mock()

        # action
        returned_value = proxy.__and__(other)

        # assert
        self.assertTupleEqual(('__and__',), wrap.call_args[0])
        self.assertTupleEqual((other,), wrap.return_value.call_args[0])
        self.assertEqual(id(wrap.return_value.return_value), id(returned_value))

    def test_or_should_call_or_via_wrap(self):
        # setup
        proxy = QuerySetProxy(mock.Mock())
        wrap = mock.Mock()
        proxy.wrap = wrap
        other = mock.Mock()

        # action
        returned_value = proxy.__or__(other)

        # assert
        self.assertTupleEqual(('__or__',), wrap.call_args[0])
        self.assertTupleEqual((other,), wrap.return_value.call_args[0])
        self.assertEqual(id(wrap.return_value.return_value), id(returned_value))

    def test_delete_should_call_query_delete(self):
        # setup
        query = mock.Mock()
        proxy = QuerySetProxy(query)
        
        # action
        proxy.delete()

        # assert
        self.assertEqual(1, query.delete.call_count)
